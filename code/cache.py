import base64
import json
import pickle
import sqlite3
import pathlib
import os
import sys

import numpy


def get_backend(args, **kwargs):
    try:
        return cache_backends[args.cache_backend](args, **kwargs)
    except IndexError as e:
        raise Exception("Invalid cache backend") from e


def file_location_from_spec(p: str):
    return p.replace(".", "/") + ".py"


class AbstractCache:
    def __init__(self, args, **kwargs):
        raise NotImplementedError

    def setup(self):
        raise NotImplementedError

    def shutdown(self):
        raise NotImplementedError

    def get(self, pair):
        raise NotImplementedError

    def insert(self, pair, avgScoreA, avgScoreB, stdevA, stdevB, firstRoundHistory, roundResultsStr):
        raise NotImplementedError

    def get_last_modified(self, pair):
        afile = pathlib.Path(file_location_from_spec(pair[0])).absolute()
        bfile = pathlib.Path(file_location_from_spec(pair[1])).absolute()
        sfile = pathlib.Path(sys.argv[0]).absolute()
        almod = os.path.getmtime(afile)
        blmod = os.path.getmtime(bfile)
        slmod = os.path.getmtime(sfile)
        mod = max(almod, blmod, slmod)
        return mod


class SQLiteCache(AbstractCache):
    default = "cache"

    def __init__(self, args, **kwargs):
        file = args.cache_file
        self.file = file if file != "" else self.default
        self.cache = sqlite3.connect(self.file)
        self.cur = self.cache.cursor()

    def setup(self):
        cache = sqlite3.connect("cache")
        self.cur.execute("PRAGMA read_uncommitted=1")
        self.cur.execute("PRAGMA journal_mode=wal")
        self.cur.execute("PRAGMA wal_autocheckpoint=0")
        self.cur.execute((
            "CREATE TABLE IF NOT EXISTS cache ("
            "moduleA text NOT NULL,"
            "moduleB text NOT NULL,"
            "result text NOT NULL,"
            "timestamp number NOT NULL )"
        ))

        cache.commit()

    def shutdown(self):
        self.cur.execute("PRAGMA wal_checkpoint(FULL)")
        self.close()

    def get(self, pair):
        mod = self.get_last_modified(pair)

        cur = self.cur

        res = cur.execute(f"SELECT result FROM cache WHERE timestamp >= ? AND moduleA = ? AND moduleB = ?",
                          (mod, pair[0], pair[1])).fetchone()
        if res:
            unpacked = pickle.loads(base64.b64decode(res[0]))
            return (unpacked.get("avgScoreA"),
                    unpacked.get("avgScoreB"),
                    unpacked.get("stdevA"),
                    unpacked.get("stdevB"),
                    numpy.array(unpacked.get("firstRoundHistory")),
                    unpacked.get("roundResultsStr"),)  # This is a tuple.
        else:
            return False

    def insert(self, pair, avgScoreA, avgScoreB, stdevA, stdevB, firstRoundHistory, roundResultsStr):
        mod = self.get_last_modified(pair)

        renc = {
            "avgScoreA": avgScoreA,
            "avgScoreB": avgScoreB,
            "stdevA": stdevA,
            "stdevB": stdevB,
            "firstRoundHistory": firstRoundHistory.tolist(),
            "roundResultsStr": roundResultsStr
        }
        rstr = base64.b64encode(pickle.dumps(renc))
        self.cur.execute("INSERT INTO cache (moduleA, moduleB, result, timestamp)"
                         "VALUES(?, ?, ?, ?)", (pair[0], pair[1], rstr, mod))

    def close(self):
        self.cur.close()
        self.cache.commit()
        self.cache.close()


class JSONCache(AbstractCache):
    default = "cache.json"

    def __init__(self, args, **kwargs):
        file = args.cache_file
        self.cache = file if file != "" else self.default
        self.lock = kwargs.get("lock")

    def setup(self):
        pass

    def shutdown(self):
        pass

    def get(self, pair):
        mod = self.get_last_modified(pair)

        try:
            with open(self.cache, "r") as file:
                cache = json.load(file)
                result = [x.get("result") for x in cache if
                          x.get("timestamp") >= mod and x.get("moduleA") == pair[0] and x.get("moduleB") == pair[1]][0]
                return (result.get("avgScoreA"),
                        result.get("avgScoreB"),
                        result.get("stdevA"),
                        result.get("stdevB"),
                        numpy.array(result.get("firstRoundHistory")),
                        result.get("roundResultsStr"),)  # This is a tuple.
        except FileNotFoundError:
            return False
        except IndexError:
            return False
        except json.JSONDecodeError:
            return False

    def insert(self, pair, avgScoreA, avgScoreB, stdevA, stdevB, firstRoundHistory, roundResultsStr):
        self.lock.acquire()
        try:
            mod = self.get_last_modified(pair)
            try:
                with open(self.cache, "r") as file:
                    cache = json.loads(file.read())
            except json.JSONDecodeError:
                cache = list()
            except FileNotFoundError:
                cache = list()

            with open(self.cache, "w") as file:
                renc = {
                    "avgScoreA": avgScoreA,
                    "avgScoreB": avgScoreB,
                    "stdevA": stdevA,
                    "stdevB": stdevB,
                    "firstRoundHistory": firstRoundHistory.tolist(),
                    "roundResultsStr": roundResultsStr
                }

                cache.append({
                    "result": renc,
                    "moduleA": pair[0],
                    "moduleB": pair[1],
                    "timestamp": mod
                })

                file.write(json.dumps(cache))
        finally:
            self.lock.release()

    def close(self):
        pass


cache_backends = {"sqlite": SQLiteCache, "json": JSONCache}

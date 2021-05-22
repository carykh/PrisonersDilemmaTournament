let names = ['FallenAngel', 'FallenAngel2', 'Priest', 'AngryPriest'];
let COLSIZE = 30;

let color = false;

let customNames = false;

for(let i=0;i<process.argv.length;i++){
  if(
    process.argv[i].indexOf('-w=')==0 ||
    process.argv[i].indexOf('-width=')==0 ||
    process.argv[i].indexOf('--width=')==0
  ){
    COLSIZE = parseInt(process.argv[i].replace('--width=','').replace('-width=','').replace('-w=',''));
  }
  if(
    process.argv[i].indexOf('-c')==0 ||
    process.argv[i].indexOf('-color')==0 ||
    process.argv[i].indexOf('--color')==0
  ){
    color = true;
  }
  if(i > 1 &&
    process.argv[i].indexOf('-')<0 &&
    process.argv[i].indexOf('/')<0 &&
    process.argv[i].indexOf('\\')<0
  ){
    if(!customNames){
      customNames = true;
      names = [];
    }
    names.push(process.argv[i]);
  }
}

const data = require('./results.json');

for (let i in data) {
  data[i].playerA.name = data[i].playerA.name.replace(/[a-zA-Z0-9]+\./, '');
  data[i].playerB.name = data[i].playerB.name.replace(/[a-zA-Z0-9]+\./, '');

  //console.log(data[i].playerA.name);
  //console.log(data[i].playerB.name);
}

function standardDeviation(a) {
  let mean = 0;
  a.map(a => mean += a);
  mean /= a.length;

  let sum = 0;
  for (let val of a) {
    sum += (val - mean) * (val - mean);
  }
  return Math.sqrt(1 / a.length * sum);
}

function compare(data, names) {
  let relevant = [];
  let participants = [];
  let participantStuff = {};
  for (let i in data) {
    if (names.indexOf(data[i].playerA.name) >= 0) {
      relevant.push(data[i]);
      if (participants.indexOf(data[i].playerB.name) < 0) {
        participants.push(data[i].playerB.name);
        participantStuff[data[i].playerB.name] = {};
      }
      participantStuff[data[i].playerB.name][data[i].playerA.name]=data[i].playerA.avgScore;
    }
    if (names.indexOf(data[i].playerB.name) >= 0) {
      relevant.push(data[i]);
      if (participants.indexOf(data[i].playerA.name) < 0) {
        participants.push(data[i].playerA.name);
        participantStuff[data[i].playerA.name] = {};
      }
      participantStuff[data[i].playerA.name][data[i].playerB.name]=data[i].playerB.avgScore;
    }
  }

  for(let i in names){
    participants.splice(participants.indexOf(names[i]),1);
  }

  function mapParticipants(a) {
    let ar = [];
    for(let v in participantStuff[a]){
      ar.push(participantStuff[a][v]);
    }
    return [a, standardDeviation(ar)];
  }

  participants = participants.map(mapParticipants).sort((a, b) => b[1] - a[1]).map(a => a[0]);

  let t1 =  "Opponent ".padStart(COLSIZE);
  let t2 = "---------".padStart(COLSIZE,'-');

  for(let n in names){
    t1 += "|"+names[n].padEnd(COLSIZE);
    t2 += "+"+"".padEnd(COLSIZE,"-");
  }

  console.log(`${t1}\n${t2}`);
  for(let i in participants){
    let t = '';
    let best = [-Infinity,[]];
    let worst = [Infinity,[]];
    for(let n in names){
      let v = participantStuff[participants[i]][names[n]];
      if(v > best[0]){
        best = [v, [names[n]]];
      }
      else if(v == best[0]){
        best[1].push(names[n]);
      }
      if(v < worst[0]){
        worst = [v, [names[n]]];
      }
      else if(v == worst[0]){
        worst[1].push(names[n]);
      }
    }
    if(best[0] == worst[0]){continue;}
    //console.log(`\n\nbest: ${best}\nworst: ${worst}\n\n`);
    for(let n in names){
      let v = participantStuff[participants[i]][names[n]];
      if(color){
        t += `|${best[1].indexOf(names[n])>=0?(worst[1].indexOf(names[n])>=0?'\x1b[100m':'\x1b[42m'):(worst[1].indexOf(names[n])>=0?'\x1b[41m':'')} `+(''+Math.round(v*1000)/1000).padEnd(COLSIZE-1)+'\x1b[0m';
      }
      else{
        if(best[1].indexOf(names[n])>=0){
          t += ("| > "+Math.round(v*1000)/1000+" <").padEnd(COLSIZE+1);
        }
        else{
          t += ("|   "+Math.round(v*1000)/1000).padEnd(COLSIZE+1);
        }
      }
    }
    console.log(`${(''+participants[i]).padEnd(COLSIZE)}${t}`);
  }
}

compare(data, names)

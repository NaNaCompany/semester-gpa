export function number(value,min,max,code='numberError'){if(String(value).trim()==='')throw Error(code);const n=Number(value);if(!Number.isFinite(n)||n<min||n>max)throw Error(code);return n;}
export function parseScale(text,max){number(max,1,10);const lines=text.trim().split(/\r?\n/);if(!text.trim()||lines.length>30)throw Error('scaleError');const scale=new Map();for(const line of lines){const parts=line.split('=');if(parts.length!==2)throw Error('scaleError');const key=parts[0].trim();if(!key||key.length>20||scale.has(key)||['PASS','EXCLUDE'].includes(key))throw Error('scaleError');scale.set(key,number(parts[1],0,max,'scaleError'));}return scale;}
export function calculate({max,scale,courses,priorCredits,priorGpa,target,futureCredits}){
 max=number(max,1,10);priorCredits=number(priorCredits,0,10000);priorGpa=number(priorGpa,0,max);target=number(target,0,max);futureCredits=number(futureCredits,.1,1000);
 if(!Array.isArray(courses)||!courses.length||courses.length>100)throw Error('courseLimit');let credits=0,quality=0,passCredits=0,oldCredits=0,oldQuality=0;const details=[];
 for(const c of courses){const cr=number(c.credits,.1,100),oc=number(c.oldCredits,0,100),op=number(c.oldPoints,0,max);if(String(c.name).length>100)throw Error('nameLimit');if(!['PASS','EXCLUDE'].includes(c.grade)&&!scale.has(c.grade))throw Error('gradeError');if(oc>0&&['PASS','EXCLUDE'].includes(c.grade))throw Error('retakeMode');if(c.grade==='PASS')passCredits+=cr;if(c.grade!=='EXCLUDE'&&c.grade!=='PASS'){const points=scale.get(c.grade);credits+=cr;quality+=cr*points;oldCredits+=oc;oldQuality+=oc*op;details.push({...c,credits:cr,points,quality:cr*points,oldCredits:oc,oldPoints:op});}else details.push({...c,credits:cr,points:null,quality:0,oldCredits:0,oldPoints:0});}
 const remainingCredits=priorCredits-oldCredits,remainingQuality=priorCredits*priorGpa-oldQuality,tolerance=1e-8;
 if(remainingCredits< -tolerance||remainingQuality< -tolerance||remainingQuality>remainingCredits*max+tolerance)throw Error('retakeError');
 const cumulativeCredits=Math.max(0,remainingCredits)+credits,cumulativeQuality=Math.max(0,remainingQuality)+quality;
 if(!cumulativeCredits)throw Error('noGraded');
 const required=(target*(cumulativeCredits+futureCredits)-cumulativeQuality)/futureCredits;
 return {credits,quality,semester:credits?quality/credits:null,passCredits,oldCredits,cumulativeCredits,cumulative:cumulativeQuality/cumulativeCredits,required,feasible:required<=max+1e-10,already:required<=0,details};
}
export function csv(rows){return '\uFEFF'+rows.map(row=>row.map(v=>{let s=String(v??'');if(/^\s*[=+@-]/.test(s))s="'"+s;return /[",\r\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;}).join(',')).join('\r\n')+'\r\n';}

import { createHash } from 'node:crypto';
import { expect, it } from 'vitest';
import concepts from '../scripts/concepts.json';
import { BASE_BANK, validateQuestion, fingerprint } from '../src/model';

it('1000 reviewed original exercises: 960 numeric in 36 families, 40 conceptual, no duplicates', () => {
 expect(BASE_BANK).toHaveLength(1000);
 expect(new Set(BASE_BANK.map(q=>q.id)).size).toBe(1000);
 expect(new Set(BASE_BANK.map(fingerprint)).size).toBe(1000);
 const numeric=BASE_BANK.filter(q=>q.calculation);
 expect(numeric).toHaveLength(960);
 expect(BASE_BANK.filter(q=>!q.calculation)).toHaveLength(40);
 expect(new Set(numeric.map(q=>q.family)).size).toBe(36);
 for(const q of BASE_BANK) {
  expect(validateQuestion(q)).toEqual(q);
  expect(q.year).toBeNull(); expect(q.session).toBeNull();
  expect(q.type).toBe('original'); expect(q.verificationStatus).toBe('reviewed');
  expect(q.reviewNote).toContain('외부');
 }
});
it('preserves every field and ID of the existing 60 questions',()=>{
 expect(createHash('sha256').update(JSON.stringify(BASE_BANK.slice(0,60))).digest('hex'))
  .toBe('f864ecdfdb000ed7ded7fdd856911994c1b72d31114831c3cf730425897034a5');
});
it('every calculation family has the documented distinct condition sets',()=>{
 const groups=new Map<string, string[]>();
 for(const q of BASE_BANK.filter(q=>q.calculation)) {
  const g=groups.get(q.family!)??[]; g.push(JSON.stringify(q.calculation!.values));groups.set(q.family!,g);
 }
 for(const [family,conditions] of groups) {
  const count=['sensible','efficiency','fuel','pressure','flow','power'].includes(family)?10:30;
  expect(conditions).toHaveLength(count);
  expect(new Set(conditions).size).toBe(count);
 }
});
const units:Record<string,string>={sensible:'kJ',efficiency:'kJ',fuel:'kJ',pressure:'kPa',flow:'m³',power:'kJ',latent:'kJ','steam-duty':'kJ','wet-steam':'kJ/kg','ideal-gas':'kg','gas-expansion':'m³','air-ratio':'배','carbon-oxygen':'kg','hydrogen-oxygen':'kg','methane-air':'m³','fuel-blend':'kJ/kg',conduction:'W',convection:'W','thermal-resistance':'m²·K/W',lmtd:'K',mixing:'℃','linear-expansion':'mm',density:'kg/m³','pump-water':'kW','pump-shaft':'kW','fan-air':'kW','pipe-speed':'m/s',hydrostatic:'kPa','absolute-pressure':'kPa','pressure-conversion':'kPa','fuel-saving':'%','flue-recovery':'kW',blowdown:'kg/h','calcium-hardness':'mg/L as CaCO₃','temperature-conversion':'℉','pump-affinity':'m'};
for (const q of BASE_BANK.filter(q=>q.calculation)) it(`${q.id}: inverse conservation equation, unit, choice and rounding`,()=>{
 const {kind,values:v,result,unit}=q.calculation!;
 const answer=parseFloat(q.choices[q.answer-1]);
 let inverse:(y:number)=>number, target:number;
 // Solve for a supplied physical input, independently from Python's forward generator.
 switch(kind) {
 case 'sensible': inverse=y=>y/v[0]/v[2];target=v[1];break;
 case 'efficiency': inverse=y=>y/v[0]*100;target=v[1];break;
 case 'fuel': inverse=y=>y/v[1];target=v[0];break;
 case 'pressure': inverse=y=>y*v[1];target=v[0];break;
 case 'flow': inverse=y=>y/v[1];target=v[0];break;
 case 'power': inverse=y=>y/3600/v[1];target=v[0];break;
 case 'latent': inverse=y=>y/v[1];target=v[0];break;
 case 'steam-duty': inverse=y=>y/v[0]+v[2];target=v[1];break;
 case 'wet-steam': inverse=y=>(y-v[0])/v[1];target=v[2];break;
 case 'ideal-gas': inverse=y=>y*v[2]*v[3]/v[1];target=v[0];break;
 case 'gas-expansion': inverse=y=>y*v[1]/v[0];target=v[2];break;
 case 'air-ratio': inverse=y=>y*v[1];target=v[0];break;
 case 'carbon-oxygen': inverse=y=>y*v[1]/v[2];target=v[0];break;
 case 'hydrogen-oxygen': inverse=y=>y*2*v[1]/v[2];target=v[0];break;
 case 'methane-air': inverse=y=>y*v[2]/v[1];target=v[0];break;
 case 'fuel-blend': inverse=y=>(y-v[2])/(v[1]-v[2]);target=v[0];break;
 case 'conduction': inverse=y=>y*v[3]/(v[0]*v[1]);target=v[2];break;
 case 'convection': inverse=y=>y/(v[0]*v[1]);target=v[2];break;
 case 'thermal-resistance': inverse=y=>(y-v[2]/v[3])*v[1];target=v[0];break;
 case 'lmtd': inverse=y=>Math.exp((v[0]-v[1])/y);target=v[0]/v[1];break;
 case 'mixing': inverse=y=>(y*(v[0]+v[2])-v[0]*v[1])/v[2];target=v[3];break;
 case 'linear-expansion': inverse=y=>y/1000/v[1]/v[0];target=v[2];break;
 case 'density': inverse=y=>y*v[1];target=v[0];break;
 case 'pump-water': inverse=y=>y*1000/v[0]/v[1]/v[3];target=v[2];break;
 case 'pump-shaft': inverse=y=>y*v[1]/100;target=v[0];break;
 case 'fan-air': inverse=y=>y*1000/v[1];target=v[0];break;
 case 'pipe-speed': inverse=y=>y*v[1];target=v[0];break;
 case 'hydrostatic': inverse=y=>y*1000/v[0]/v[1];target=v[2];break;
 case 'absolute-pressure': inverse=y=>y-v[1];target=v[0];break;
 case 'pressure-conversion': inverse=y=>y/v[1];target=v[0];break;
 case 'fuel-saving': inverse=y=>v[0]*(1-y/100);target=v[1];break;
 case 'flue-recovery': inverse=y=>y/v[0]/v[1];target=v[2];break;
 case 'blowdown': inverse=y=>y*(v[1]-v[0])/v[2];target=v[0];break;
 case 'calcium-hardness': inverse=y=>y*v[2]/v[1];target=v[0];break;
 case 'temperature-conversion': inverse=y=>(y-v[2])/v[1];target=v[0];break;
 case 'pump-affinity': inverse=y=>v[0]*Math.sqrt(y/v[2]);target=v[1];break;
 default: throw Error('unknown calculation family');
 }
 expect(Number.isFinite(result)).toBe(true);
 expect(inverse(result)).toBeCloseTo(target,7);
 // The correct choice's displayed rounding interval must contain the independent solution.
 const interval=[inverse(answer-.005001),inverse(answer+.005001)].sort((a,b)=>a-b);
 expect(target).toBeGreaterThanOrEqual(interval[0]);expect(target).toBeLessThanOrEqual(interval[1]);
 expect(Math.abs(answer-result)).toBeLessThanOrEqual(.00500001);
 expect(unit).toBe(units[kind]);
 expect(q.choices.every(c=>c.endsWith(` ${unit}`))).toBe(true);
 expect(q.choices.filter(c=>Math.abs(parseFloat(c)-result)<=.00500001)).toHaveLength(1);
 expect(new Set(q.choices.map(parseFloat)).size).toBe(4);
 expect(q.explanation).toContain(q.choices[q.answer-1]);
});
for (const [i,c] of concepts.entries()) it(`concept ${i+1}: manuscript answer retained with four distinct choices`,()=>{
 const q=BASE_BANK.find(q=>q.id===`ENERGY-CONCEPT-${String(i+1).padStart(3,'0')}`)!;
 expect(q.calculation).toBeUndefined();expect(q.family).toBeUndefined();
 expect(q.choices[q.answer-1]).toBe(c.choices[0]);
 expect(new Set(q.choices).size).toBe(4);expect(q.explanation).toBe(c.explanation);
});

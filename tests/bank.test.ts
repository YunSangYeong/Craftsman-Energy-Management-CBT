import { expect, it } from 'vitest';
import { BASE_BANK, validateQuestion, fingerprint } from '../src/model';
it('60 internally reviewed original exercises, 6 families, no duplicate IDs/content', () => {
 expect(BASE_BANK).toHaveLength(60);
 expect(new Set(BASE_BANK.map(q=>q.id)).size).toBe(60);
 expect(new Set(BASE_BANK.map(fingerprint)).size).toBe(60);
 expect(new Set(BASE_BANK.map(q=>q.family)).size).toBe(6);
 for(const q of BASE_BANK) { expect(validateQuestion(q)).toEqual(q); expect(q.year).toBeNull(); expect(q.session).toBeNull(); expect(q.type).toBe('original'); expect(q.verificationStatus).toBe('reviewed'); }
});
for (const q of BASE_BANK) it(`${q.id}: independent inverse equation, units and answer`,()=>{
 const {kind,values:v,result,unit}=q.calculation!;
 const answer=parseFloat(q.choices[q.answer-1]);
 expect(answer).toBeCloseTo(result,2);
 // Inverse equations avoid reusing the forward generator's computation.
 switch(kind) {
 case 'sensible': expect(answer / v[0] / v[2]).toBeCloseTo(v[1],8); expect(unit).toBe('kJ'); break;
 case 'efficiency': expect(answer/v[0]*100).toBeCloseTo(v[1],8); break;
 case 'fuel': expect(answer/v[1]).toBeCloseTo(v[0],8); break;
 case 'pressure': expect(answer*v[1]).toBeCloseTo(v[0],8); expect(unit).toBe('kPa'); break;
 case 'flow': expect(answer/v[1]).toBeCloseTo(v[0],8); expect(unit).toBe('m³'); break;
 case 'power': expect(answer/3600/v[1]).toBeCloseTo(v[0],8); break;
 default: throw Error('unknown calculation family');
 }
 expect(q.choices.filter(c=>Math.abs(parseFloat(c)-result)<0.005)).toHaveLength(1);
 expect(new Set(q.choices.map(parseFloat)).size).toBe(4);
 expect(q.explanation).toContain(result.toFixed(2));
});

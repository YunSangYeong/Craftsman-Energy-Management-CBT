"""Deterministic authored exercises; no external exam questions. No random seed needed."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
bank=[]
for n in range(1,11):
 m=10+n*2; dt=10+n; eff=60+n*2; fuel=20+n; area=2+n; force=area*(100+n*10); flow=10+n; hours=2+n; power=5+n
 cases=[
 ('sensible','현열', [m,4.2,dt],m*4.2*dt,'kJ',f'물 {m} kg을 {dt} K만큼 가열한다. 비열은 4.2 kJ/(kg·K)로 일정하고 증발과 열손실이 없을 때 필요한 열량은?',f'현열 Q = mcΔT. 질량 {m} kg × 비열 4.2 kJ/(kg·K) × 온도차 {dt} K = {m*4.2*dt:.2f} kJ. 온도차 1 K는 온도차 1 ℃와 같다.'),
 ('efficiency','보일러 효율',[1000+n*100,eff],(1000+n*100)*eff/100,'kJ',f'보일러 연료 투입 열량은 {1000+n*100} kJ이고 열효율은 {eff}%이다. 유효하게 이용한 열량은?',f'효율 = 유효 열량 / 투입 열량 × 100. 유효 열량 = {1000+n*100} × {eff}/100 = {(1000+n*100)*eff/100:.2f} kJ.'),
 ('fuel','연료 열량',[fuel,42000],fuel*42000,'kJ',f'저위발열량 42,000 kJ/kg인 연료 {fuel} kg이 완전 연소한다. 저위발열량 기준 투입 열량은?',f'투입 열량 = 연료 질량 × 저위발열량 = {fuel} kg × 42,000 kJ/kg = {fuel*42000:.2f} kJ. 보일러의 실제 유효 열량은 효율을 별도로 반영한다.'),
 ('pressure','압력',[force,area],force/area,'kPa',f'면적 {area} m²에 수직으로 균일한 힘 {force} kN이 작용한다. 이 힘에 의한 압력은?',f'압력 p = F/A = {force} kN / {area} m² = {force/area:.2f} kPa. 1 kN/m² = 1 kPa이다. 절대압력과 게이지압력의 변환 문제는 아니다.'),
 ('flow','유량',[flow,hours],flow*hours,'m³',f'체적 유량 {flow} m³/h가 {hours}시간 동안 일정하게 유지된다. 통과한 유체의 체적은?',f'체적 V = 체적 유량 × 시간 = {flow} m³/h × {hours} h = {flow*hours:.2f} m³. 누설 없이 유량이 일정한 조건이다.'),
 ('power','열출력',[power,hours],power*hours*3600,'kJ',f'일정한 열출력 {power} kW인 가열기가 {hours}시간 작동한다. 방출한 총 열량은?',f'1 kW = 1 kJ/s이고 {hours} h = {hours*3600} s. Q = 출력 × 시간 = {power} × {hours*3600} = {power*hours*3600:.2f} kJ. 대상 물체의 흡수 열량은 손실에 따라 다를 수 있다.')]
 for i,(kind,topic,values,result,unit,question,explanation) in enumerate(cases):
  correct=n%4; choices=[f'{result*x:.2f} {unit}' for x in [0.5,1.5,2,3]];choices[correct]=f'{result:.2f} {unit}'
  bank.append(dict(id=f'ENERGY-{kind}-{n:02}',subject='열설비 설치·운전 및 관리',topic=topic,question=question,choices=choices,answer=correct+1,explanation=explanation,difficulty='하',year=None,session=None,type='original',sourceUrl='https://github.com/YunSangYeong/Craftsman-Energy-Management-CBT/blob/main/docs/question-review.md',verificationStatus='reviewed',reviewNote='AI 일반 지식으로 작성. 조건·단위·공식·해설 문장 내부 검토 및 독립 역산 테스트. 외부 전문가 검수·공식 출제기준 대조 미완료.',version='main',rights='본 프로젝트 자체 제작 · CC BY 4.0 · 출처 표시 및 변경 표시',family=kind,calculation=dict(kind=kind,values=values,result=result,unit=unit,precision=2)))
from expanded_bank import build_expansion
bank.extend(build_expansion())
assert len(bank) == 1000
(root/'src/data').mkdir(exist_ok=True)
(root/'src/data/questions.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
example={**bank[0],'id':'IMPORT-EXAMPLE-001','verificationStatus':'pending','reviewNote':'양식 예제: 등록 전 독립 검토 필요','question':'물 25 kg을 20 K 가열한다. 비열 4.2 kJ/(kg·K), 증발과 손실이 없을 때 필요한 열량은?','choices':['1050.00 kJ','2100.00 kJ','3150.00 kJ','4200.00 kJ'],'answer':2,'explanation':'Q = mcΔT = 25 × 4.2 × 20 = 2100.00 kJ. 상변화와 열손실은 없다.'}
(root/'public/templates/questions.json').write_text(json.dumps([example],ensure_ascii=False,indent=2)+'\n')
import csv
with (root/'public/templates/questions.csv').open('w') as f:
 fields=['id','subject','topic','question','answer','explanation','difficulty','year','session','type','sourceUrl','verificationStatus','reviewNote','version','rights','choice1','choice2','choice3','choice4']
 writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");writer.writeheader();writer.writerow({**{k:example[k] for k in fields if k in example},**{f'choice{i+1}':c for i,c in enumerate(example['choices'])}})

"""Authored learning exercises. Formula assumptions are explicit, not official exam quotations."""
import json
import math
from pathlib import Path

SOURCE = 'https://github.com/YunSangYeong/Craftsman-Energy-Management-CBT/blob/main/docs/question-review.md'


def record(identifier, topic, question, choices, answer, explanation):
    return dict(id=identifier, subject='열설비 설치·운전 및 관리', topic=topic,
                question=question, choices=choices, answer=answer, explanation=explanation,
                difficulty='중', year=None, session=None, type='original', sourceUrl=SOURCE,
                verificationStatus='reviewed',
                reviewNote='AI 일반 지식 기반 자체 제작. 가정·단위·정답·오답 보기·해설 내부 검토. 계산형은 별도 역산 검사. 외부 전문가 검수 및 공식 출제기준 대조 미완료.',
                version='main', rights='본 프로젝트 자체 제작 · CC BY 4.0 · 출처 및 변경 표시')


def build_expansion():
    bank = []
    for n in range(1, 31):
        a = 10 + n
        dt = 20 + n
        eta = 60 + n
        cases = []

        def add(kind, topic, values, result, unit, question, working, condition):
            cases.append((kind, topic, values, result, unit, question,
                          f'{condition} {working} = {result:.2f} {unit}. 최종값만 소수 둘째 자리로 반올림한다.'))

        add('latent', '증발 잠열', [a, 2257], a*2257, 'kJ',
            f'포화수 {a} kg이 같은 압력의 포화증기로 전부 변한다. 주어진 증발 잠열은 2257 kJ/kg이다. 이 상변화에 필요한 열량은?',
            f'잠열 Q = mr = {a} kg × 2257 kJ/kg', '온도 상승에 필요한 현열과 열손실은 제외한다.')
        add('steam-duty', '증기 발생 열량', [a, 2780, 420+n], a*(2780-420-n), 'kJ',
            f'급수 엔탈피 {420+n} kJ/kg, 발생 증기 엔탈피 2780 kJ/kg이다. 급수 {a} kg을 해당 증기로 만드는 데 유체가 받아야 하는 열량은?',
            f'Q = m(h증기−h급수) = {a} × (2780−{420+n})', '주어진 엔탈피는 문제의 조건값이다. 블로다운·운동 및 위치에너지 변화는 무시하고 연료 투입 열량과 구별한다.')
        x = (60+n)/100
        add('wet-steam', '습증기 건도', [500, 2100, x], 500+x*2100, 'kJ/kg',
            f'어떤 포화압력에서 포화수 엔탈피 hf=500 kJ/kg, 증발 잠열 hfg=2100 kJ/kg이다. 건도 {x:.2f}인 습증기의 비엔탈피는?',
            f'h = hf + xhfg = 500 + {x:.2f} × 2100', '건도는 전체 질량 중 증기 질량의 비율이며 과열증기에는 이 식을 적용하지 않는다.')
        p, volume, temp = 100+n*2, 2+n/10, 280+n
        add('ideal-gas', '기체 상태', [p, volume, .287, temp], p*volume/(.287*temp), 'kg',
            f'공기를 이상기체로 본다. 절대압력 {p} kPa, 체적 {volume:.1f} m³, 절대온도 {temp} K, 기체상수 0.287 kJ/(kg·K)일 때 질량은?',
            f'm = pV/(RT) = {p} × {volume:.1f} /(0.287 × {temp})', 'pV의 단위 kPa·m³는 kJ이다. 게이지압력이나 섭씨온도를 직접 넣지 않는다.')
        t1, t2 = 280+n, 400+n*2
        add('gas-expansion', '기체 체적 변화', [a, t1, t2], a*t2/t1, 'm³',
            f'일정한 압력에서 질량이 일정한 이상기체의 체적은 {t1} K에서 {a} m³이다. {t2} K로 가열한 뒤의 체적은?',
            f'V₂ = V₁T₂/T₁ = {a} × {t2}/{t1}', '압력과 기체 질량이 일정하므로 V/T가 일정하다. 온도는 K로 주어졌다.')
        theoretical, actual = 100+n*5, (100+n*5)*(1+n/100)
        add('air-ratio', '공기비', [actual, theoretical], actual/theoretical, '배',
            f'같은 기준 상태에서 이론공기량은 {theoretical} m³, 실제 공급공기량은 {actual:.2f} m³이다. 실제공기량/이론공기량으로 정의한 공기비는?',
            f'공기비 λ = A실제/A이론 = {actual:.2f}/{theoretical}', '공기비는 무차원 비율이다. 여기서 배는 비율을 표시하며 과잉공기율(%)과 다르다.')
        add('carbon-oxygen', '탄소 연소', [a, 12, 32], a*32/12, 'kg',
            f'순수 탄소 {a} kg이 C+O₂→CO₂로 완전 연소한다. 탄소와 산소 분자의 몰질량을 각각 12, 32 kg/kmol로 할 때 필요한 산소 질량은?',
            f'mO₂ = mC × 32/12 = {a} × 32/12', '산소 질량을 구하는 문제이며 공기 중 질소의 질량은 포함하지 않는다.')
        add('hydrogen-oxygen', '수소 연소', [a, 2, 32], a*32/4, 'kg',
            f'순수 수소(H₂) {a} kg이 2H₂+O₂→2H₂O로 완전 연소한다. H₂와 O₂의 몰질량을 각각 2, 32 kg/kmol로 할 때 필요한 산소 질량은?',
            f'mO₂ = (mH₂/2) × (1/2) × 32 = {a} × 8', '수소 2 kmol에 산소 1 kmol이 반응한다. 산소 부피나 공기 질량을 묻는 것이 아니다.')
        add('methane-air', '메탄 이론공기량', [a, 2, .21], a*2/.21, 'm³',
            f'CH₄+2O₂→CO₂+2H₂O 반응으로 메탄 {a} m³을 완전 연소한다. 모든 기체 부피는 같은 온도·압력 기준이고 공기의 산소 체적분율은 0.21이다. 이론공기 체적은?',
            f'A이론 = 2V메탄/0.21 = 2 × {a}/0.21', '이상기체의 반응 몰비를 같은 기준 상태의 체적비로 적용한다. 과잉공기는 포함하지 않는다.')
        f = (20+n)/100
        add('fuel-blend', '혼합연료 발열량', [f, 40000, 30000], f*40000+(1-f)*30000, 'kJ/kg',
            f'질량분율 {f:.2f}인 연료 A와 나머지 연료 B를 혼합한다. 저위발열량은 A가 40000 kJ/kg, B가 30000 kJ/kg이다. 혼합물의 저위발열량은?',
            f'H = wA HA + (1−wA)HB = {f:.2f} × 40000 + {1-f:.2f} × 30000', '혼합에 따른 화학반응이나 발열량 변화가 없다고 가정하며 질량 기준으로 평균한다.')
        k, area, length = .04, 2+n/10, .05+n/1000
        add('conduction', '평판 전도', [k, area, dt, length], k*area*dt/length, 'W',
            f'열전도율 {k} W/(m·K), 면적 {area:.1f} m², 두께 {length:.3f} m인 평판의 양 표면 온도차가 {dt} K이다. 정상상태 1차원 전도 열전달률은?',
            f'Q̇ = kAΔT/L = {k} × {area:.1f} × {dt}/{length:.3f}', '열전도율은 일정하며 평판 양 표면 사이 전도만 계산한다. 대류·접촉 열저항은 제외한다.')
        h, area = 10+n, 2+n/10
        add('convection', '표면 대류', [h, area, dt], h*area*dt, 'W',
            f'표면과 주위 유체의 온도차 {dt} K, 면적 {area:.1f} m², 대류 열전달계수 {h} W/(m²·K)일 때 대류로 전달되는 열전달률의 크기는?',
            f'Q̇ = hAΔT = {h} × {area:.1f} × {dt}', '주어진 대류계수가 일정하며 복사열은 별도로 포함하지 않는다.')
        l1, l2 = .02+n/1000, .03+n/1000
        add('thermal-resistance', '복합벽 열저항', [l1, .04, l2, .06], l1/.04+l2/.06, 'm²·K/W',
            f'두 평판층이 열 흐름 방향으로 직렬이다. 첫 층 두께 {l1:.3f} m·열전도율 0.04 W/(m·K), 둘째 층 두께 {l2:.3f} m·열전도율 0.06 W/(m·K)이다. 단위 면적당 전도 열저항 합은?',
            f'R″ = L₁/k₁ + L₂/k₂ = {l1:.3f}/0.04 + {l2:.3f}/0.06', '정상 1차원 전도이며 대류 및 층간 접촉 저항을 무시한다. 전체 면적 A에 대한 저항 K/W와 구별한다.')
        d1, d2 = 50+n, 20+n
        add('lmtd', '열교환기 평균온도차', [d1, d2], (d1-d2)/math.log(d1/d2), 'K',
            f'열교환기 양 끝의 유체 간 온도차가 각각 {d1} K와 {d2} K이다. 자연로그를 사용하는 대수평균온도차는?',
            f'ΔTlm = (ΔT₁−ΔT₂)/ln(ΔT₁/ΔT₂) = ({d1}−{d2})/ln({d1}/{d2})', '두 끝 온도차는 양수이고 서로 다르며 산술평균과 구별한다.')
        m1, m2, t1, t2 = a, a+5, 70+n/2, 10+n/2
        add('mixing', '물 혼합 열평형', [m1, t1, m2, t2], (m1*t1+m2*t2)/(m1+m2), '℃',
            f'물 {m1} kg(온도 {t1:.1f} ℃)과 물 {m2} kg(온도 {t2:.1f} ℃)을 단열 용기에서 혼합한다. 두 물의 비열은 같고 일정하다. 최종 평형 온도는?',
            f'T = (m₁T₁+m₂T₂)/(m₁+m₂) = ({m1} × {t1:.1f} + {m2} × {t2:.1f})/({m1}+{m2})', '증발·상변화가 없고 용기 열용량과 외부 열교환은 무시한다.')
        add('linear-expansion', '배관 열팽창', [a, .000012, dt], a*.000012*dt*1000, 'mm',
            f'길이 {a} m인 배관의 온도가 {dt} K 상승한다. 선팽창계수 0.000012 /K가 일정하고 자유롭게 늘어날 때 길이 증가량은?',
            f'ΔL = αLΔT = 0.000012 × {a} × {dt} m, mm로 바꾸면 1000배', '구속에 의한 응력은 계산하지 않고 미소 선팽창식을 적용한다.')
        mass, volume = 100+n*10, .1+n/200
        add('density', '밀도', [mass, volume], mass/volume, 'kg/m³',
            f'어떤 액체 시료의 질량이 {mass} kg, 체적이 {volume:.3f} m³이다. 이 상태에서 액체의 밀도는?',
            f'ρ = m/V = {mass}/{volume:.3f}', '비중은 물 밀도에 대한 비이고 밀도 자체는 질량/체적이다.')
        q, head = (5+n)/1000, 10+n
        add('pump-water', '펌프 수동력', [1000, 9.8, q, head], 1000*9.8*q*head/1000, 'kW',
            f'물의 밀도 1000 kg/m³, g=9.8 m/s²이다. 체적 유량 {q:.3f} m³/s, 총양정 {head} m인 펌프가 물에 전달하는 수동력은?',
            f'P수동력 = ρgQH/1000 = 1000 × 9.8 × {q:.3f} × {head}/1000', 'ρgQH는 W이므로 1000으로 나누어 kW로 표시한다. 축동력은 효율을 추가로 고려한다.')
        hydraulic = 2+n/10
        add('pump-shaft', '펌프 축동력', [hydraulic, eta], hydraulic/(eta/100), 'kW',
            f'펌프가 유체에 전달하는 수동력이 {hydraulic:.1f} kW이고 펌프 효율이 {eta}%이다. 펌프에 공급해야 하는 축동력은?',
            f'P축 = P수동력/η = {hydraulic:.1f}/({eta}/100)', '모터 전기효율은 별도로 고려하지 않는다. 100% 미만의 효율에서는 축동력이 수동력보다 크다.')
        q, dp = 1+n/10, 200+n*10
        add('fan-air', '송풍기 공기동력', [q, dp], q*dp/1000, 'kW',
            f'송풍기의 체적 유량은 {q:.1f} m³/s, 전압력 상승은 {dp} Pa이다. 압축성 영향을 무시할 때 공기에 전달되는 동력은?',
            f'P공기 = QΔp/1000 = {q:.1f} × {dp}/1000', 'Pa·m³/s = W이며 송풍기 축동력과는 구별한다. 입출구의 체적 변화는 무시한다.')
        q, area = .01+n/1000, .005
        add('pipe-speed', '관내 평균유속', [q, area], q/area, 'm/s',
            f'가득 찬 관에서 비압축성 유체가 정상 유동한다. 체적 유량 {q:.3f} m³/s, 관의 내부 단면적 {area} m²일 때 단면 평균유속은?',
            f'v = Q/A = {q:.3f}/{area}', '평균유속을 구하며 관벽의 국소 유속이나 유량의 질량 기준과 구별한다.')
        height = 1+n/10
        add('hydrostatic', '정수압', [1000, 9.8, height], 1000*9.8*height/1000, 'kPa',
            f'밀도 1000 kg/m³의 정지한 물에서 자유 수면보다 {height:.1f} m 아래 지점의 압력이 수면 압력보다 얼마나 높은가? g=9.8 m/s²이다.',
            f'Δp = ρgh/1000 = 1000 × 9.8 × {height:.1f}/1000', 'ρgh는 Pa이므로 kPa로 변환한다. 대기압을 더한 절대압력이 아닌 수두에 의한 압력차이다.')
        gauge = 100+n*10
        add('absolute-pressure', '절대압력과 게이지압력', [gauge, 101], gauge+101, 'kPa',
            f'대기압이 101 kPa인 장소에서 압력계의 게이지압력이 {gauge} kPa이다. 절대압력은?',
            f'p절대 = p게이지 + p대기 = {gauge} + 101', '게이지압력은 주변 대기압을 기준으로 측정하며 모든 압력의 단위는 kPa이다.')
        mpa = .1+n/100
        add('pressure-conversion', '압력 단위 환산', [mpa, 1000], mpa*1000, 'kPa',
            f'압력 {mpa:.2f} MPa를 kPa로 환산한 값은?',
            f'p(kPa) = p(MPa) × 1000 = {mpa:.2f} × 1000', '1 MPa = 10⁶ Pa, 1 kPa = 10³ Pa이다. 압력 기준(절대/게이지)을 바꾸는 변환은 아니다.')
        old, new = 1000+n*10, 800+n*5
        add('fuel-saving', '연료 절감률', [old, new], (old-new)/old*100, '%',
            f'동일한 유효 열량을 생산하는 데 개선 전 연료 {old} kg, 개선 후 {new} kg이 필요했다. 개선 전 소비량 기준 연료 절감률은?',
            f'절감률 = (B전−B후)/B전 × 100 = ({old}−{new})/{old} × 100', '동일 연료·동일 유효 생산량 조건이며 보일러 열효율 자체와 혼동하지 않는다.')
        mdot, cp, delta = 1+n/10, 1.1, 50+n
        add('flue-recovery', '배기가스 현열 회수', [mdot, cp, delta], mdot*cp*delta, 'kW',
            f'질량 유량 {mdot:.1f} kg/s인 배기가스를 {delta} K 냉각한다. 평균 정압비열 1.1 kJ/(kg·K)가 일정하고 응축이 없다. 회수 가능한 현열률은?',
            f'Q̇ = ṁcpΔT = {mdot:.1f} × 1.1 × {delta}', 'kJ/s = kW이다. 수증기 응축 잠열과 외부 손실은 포함하지 않는다.')
        feed, boiler, steam = 50+n, 1000+n*10, 1000+n*20
        add('blowdown', '연속 블로다운 물질수지', [feed, boiler, steam], feed*steam/(boiler-feed), 'kg/h',
            f'정상상태 보일러에서 급수의 용존 고형분 질량농도 {feed} mg/kg, 보일러수 농도 {boiler} mg/kg, 증기 발생량 {steam} kg/h이다. 고형분이 증기에 전혀 섞이지 않으면 필요한 연속 블로다운 질량 유량은?',
            f'급수 F=S+B, 고형분 수지 Cf(S+B)=CbB. 따라서 B=CfS/(Cb−Cf) = {feed} × {steam}/({boiler}−{feed})', '침전·약품 첨가·누출이 없는 이상 수지이다. 주어진 농도는 법적 관리 기준이 아니다.')
        ca = 10+n
        add('calcium-hardness', '칼슘 경도 환산', [ca, 100, 40], ca*100/40, 'mg/L as CaCO₃',
            f'물의 Ca²⁺ 질량농도가 {ca} mg/L이고 다른 경도 성분은 없다. Ca와 CaCO₃의 몰질량을 각각 40, 100 g/mol로 할 때 CaCO₃ 환산 경도는?',
            f'칼슘과 CaCO₃는 1 mol당 같은 2가 당량을 가지므로 경도 = {ca} × 100/40', '경도 성분의 CaCO₃ 상당량이며 실제 탄산칼슘이 모두 녹아 있다는 뜻은 아니다.')
        c = 10+n
        add('temperature-conversion', '온도 눈금', [c, 1.8, 32], c*1.8+32, '℉',
            f'섭씨온도 {c} ℃를 화씨온도로 환산한 값은?',
            f'T(℉) = (9/5)T(℃)+32 = 1.8 × {c}+32', '절대 온도 눈금 변환이며 온도차만 변환할 때는 32를 더하지 않는다.')
        oldspeed, newspeed, oldhead = 1000, 1000+n*10, 10+n
        add('pump-affinity', '펌프 상사법칙', [oldspeed, newspeed, oldhead], oldhead*(newspeed/oldspeed)**2, 'm',
            f'동일한 원심펌프·같은 임펠러 지름에서 상사 운전점을 비교한다. 회전수 {oldspeed} rpm에서 양정 {oldhead} m였다. 회전수 {newspeed} rpm에서 양정은? 양정은 회전수 제곱에 비례한다고 가정한다.',
            f'H₂ = H₁(N₂/N₁)² = {oldhead} × ({newspeed}/{oldspeed})²', '상사법칙이 성립하는 조건이며 고정된 실제 배관계의 운전점 변화 전체를 보증하지 않는다.')

        assert len(cases) == 30
        for i, (kind, topic, values, result, unit, question, explanation) in enumerate(cases):
            # Preserve precision and keep all distractors numerically distinct after rounding.
            answer = (n+i) % 4
            choices = [f'{result*factor:.2f} {unit}' for factor in [.5, 1.5, 2, 3]]
            choices[answer] = f'{result:.2f} {unit}'
            assert len(set(choices)) == 4 and result > 0
            q = record(f'ENERGY-{kind}-{n:02}', topic,
                       question+' (계산값은 소수 둘째 자리까지 표시)', choices, answer+1, explanation)
            q.update(family=kind, calculation=dict(kind=kind, values=values, result=result, unit=unit, precision=2))
            bank.append(q)

    concepts = json.loads((Path(__file__).parent/'concepts.json').read_text())
    assert len(concepts) == 40
    for i, c in enumerate(concepts, 1):
        # Manuscript lists correct choice first; rotate, retaining stable IDs.
        offset = i % 4
        choices = c['choices'][offset:]+c['choices'][:offset]
        bank.append(record(f'ENERGY-CONCEPT-{i:03}', c['topic'], c['question'], choices,
                           choices.index(c['choices'][0])+1, c['explanation']))
    return bank

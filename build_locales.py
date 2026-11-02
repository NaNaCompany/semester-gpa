import pathlib,json

# Shared book banner adapter; the campaign itself is maintained in src_cdn.
def _shared_book_banner(value):
    if isinstance(value, dict) and any(isinstance(key, str) and key.endswith('.html') for key in value):
        return {key: _shared_book_banner(item) for key, item in value.items()}
    if not isinstance(value, str) or not value.lstrip('\ufeff \r\n\t').lower().startswith(('<!doctype html', '<html')) or 'https://nanalab.kr/src_cdn/banner/astra.js' in value:
        return value
    snippet = '<!-- NaNa shared book banner --><script defer src="https://nanalab.kr/src_cdn/banner/astra.js"></script><!-- /NaNa shared book banner -->'
    import re
    opening = re.search(r'<head\b[^>]*>', value, re.I)
    if opening:
        return value[:opening.end()] + snippet + value[opening.end():]
    for closing in ['</body>', '</html>']:
        at = value.lower().find(closing)
        if at >= 0:
            return value[:at] + snippet + value[at:]
    return value + snippet

root=pathlib.Path(__file__).parent
langs=['ko','en','es','zh','ja','de']
data=r'''title|학기 성적 시뮬레이터|Semester GPA Simulator|Simulador de promedio académico|学期绩点模拟器|学期成績シミュレーター|Semester-Notensimulator
hero|이번 학기 성적,\n목표까지 계산하기.|Plan this semester.\nSee what your goal needs.|Planifica el semestre.\nCalcula tu objetivo.|模拟本学期成绩，\n计算目标所需绩点。|今学期の成績から、\n目標まで計算。|Semester planen.\nZielnote berechnen.
intro|직접 정한 환산표와 학점으로 평균을 계산합니다. 학교 공식 성적표가 아닌 개인 시나리오입니다.|Calculate credit-weighted averages with your own grading scale. A personal scenario, not an official transcript.|Calcula promedios por créditos con tu escala. Es un escenario personal, no un expediente oficial.|按自定义换算表与学分计算加权平均，仅供个人模拟，并非学校官方成绩单。|独自の換算表と単位数で加重平均を計算。大学の公式成績表ではなく個人用の試算です。|Gewichtete Durchschnitte mit eigener Notentabelle. Persönliches Szenario, kein offizielles Zeugnis.
settings|나의 환산 규칙|Your grading rules|Tus reglas de calificación|自定义换算规则|自分の換算ルール|Eigene Bewertungsregeln
max|만점|Maximum GPA|Promedio máximo|满分绩点|満点|Maximaler Notenwert
scale|환산표 (등급=점수, 한 줄에 하나)|Scale (grade=points, one per line)|Escala (nota=puntos, una por línea)|换算表（等级=分数，每行一项）|換算表（評価=点、1 行に 1 件）|Tabelle (Note=Punkte, eine je Zeile)
scaleHint|예시 환산표는 임의 정책입니다. 소속 대학 규칙으로 직접 고치세요.|The sample scale is illustrative. Replace it with your institution's rules.|La escala es ilustrativa. Sustitúyela por las reglas de tu institución.|示例换算表仅作演示，请自行按学校规则修改。|サンプルは仮のルールです。所属大学の規則に合わせて編集してください。|Die Beispieltabelle ist frei gewählt. An die Regeln deiner Hochschule anpassen.
priorCredits|이전 누적 평점 반영 학점|Previous GPA-bearing credits|Créditos previos computables|此前计入绩点的累计学分|過去の GPA 対象単位|Bisherige benotete Leistungspunkte
priorGpa|이전 누적 평점|Previous cumulative GPA|Promedio acumulado previo|此前累计绩点|過去の累積 GPA|Bisheriger Notendurchschnitt
courses|이번 학기 과목|This semester's courses|Asignaturas del semestre|本学期课程|今学期の科目|Kurse dieses Semesters
course|과목명|Course|Asignatura|课程名|科目名|Kursname
credits|학점|Credits|Créditos|学分|単位数|Leistungspunkte
grade|등급|Grade|Nota|等级|評価|Note
oldCredits|재수강 이전 학점 (0=해당 없음)|Replaced credits (0=none)|Créditos reemplazados (0=ninguno)|重修前学分（0=无）|再履修前の単位（0=なし）|Ersetzte Punkte (0=keine)
oldPoints|재수강 이전 환산점수|Replaced grade points|Puntos de la nota reemplazada|重修前换算分数|再履修前の換算点|Ersetzter Notenwert
add|과목 추가|Add course|Añadir asignatura|添加课程|科目を追加|Kurs hinzufügen
remove|삭제|Remove|Eliminar|删除|削除|Entfernen
pass|P/F · 평점 제외|Pass/fail · excluded from GPA|Aprobado/reprobado · sin promedio|通过/不通过 · 不计绩点|合否科目 · GPA 対象外|Bestanden/nicht bestanden · ohne Notenwert
excludedCourse|계산 제외|Exclude course|Excluir asignatura|排除课程|計算対象外|Kurs ausschließen
retakeHint|재수강은 이전 누적값에 포함된 학점·환산점수를 직접 입력합니다. 해당 이전 기록을 빼고 새 성적을 반영합니다. 같은 이전 기록을 중복 지정하지 마세요.|For a retake, enter credits and points already included in the previous totals. That record is removed before the new grade is added. Do not replace the same record twice.|Para repetir una asignatura, indica créditos y puntos ya incluidos en el acumulado. Se elimina ese registro y se añade la nota nueva. No reemplaces el mismo registro dos veces.|重修时填写已计入此前累计值的旧学分和旧分数，先扣除旧记录再计入新成绩，请勿重复指定同一旧记录。|再履修は過去の累積値に含まれる単位・換算点を入力。古い記録を除き新成績を加えます。同じ過去の記録を重複指定しないでください。|Bei Wiederholung bereits enthaltene Punkte und Notenwert eingeben. Der alte Eintrag wird vor der neuen Note abgezogen. Denselben Eintrag nicht doppelt ersetzen.
targetTitle|다음 학기 목표 시나리오|Next semester target|Objetivo del próximo semestre|下学期目标模拟|次学期の目標シナリオ|Ziel für nächstes Semester
target|목표 누적 평점|Target cumulative GPA|Promedio acumulado objetivo|目标累计绩点|目標累積 GPA|Angestrebter Gesamtdurchschnitt
futureCredits|앞으로 추가할 평점 반영 학점|Future GPA-bearing credits|Créditos futuros computables|未来新增计入绩点的学分|今後追加する GPA 対象単位|Künftige benotete Leistungspunkte
calculate|시나리오 계산|Calculate scenario|Calcular escenario|计算模拟|シナリオを計算|Szenario berechnen
result|계산 결과|Scenario results|Resultados|计算结果|計算結果|Ergebnisse
semester|이번 학기 평점|Semester GPA|Promedio del semestre|本学期绩点|今学期の GPA|Semesterdurchschnitt
cumulative|예상 누적 평점|Projected cumulative GPA|Promedio acumulado previsto|预计累计绩点|予想累積 GPA|Erwarteter Gesamtdurchschnitt
required|목표에 필요한 다음 평균|Required future average|Promedio futuro necesario|目标所需未来平均绩点|目標に必要な今後の平均|Benötigter künftiger Durchschnitt
quality|학점 × 환산점수|Credits × points|Créditos × puntos|学分 × 换算分数|単位 × 換算点|Leistungspunkte × Notenwert
download|결과 CSV 다운로드|Download result CSV|Descargar CSV|下载结果 CSV|結果 CSV をダウンロード|Ergebnis als CSV herunterladen
initial|예제를 확인하고 나만의 정책으로 수정하세요.|Try the example, then edit your own policy.|Prueba el ejemplo y ajusta tus reglas.|查看示例后修改为自己的规则。|サンプルを確認し、自分のルールに変更してください。|Beispiel prüfen und eigene Regeln eintragen.
changed|입력이 변경되었습니다. 다시 계산하세요.|Input changed. Calculate again.|La entrada cambió. Calcula de nuevo.|输入已更改，请重新计算。|入力が変更されました。再計算してください。|Eingabe geändert. Erneut berechnen.
complete|계산 완료|Calculation complete|Cálculo completado|计算完成|計算完了|Berechnung abgeschlossen
impossible|입력한 학점과 만점으로는 목표에 도달할 수 없습니다.|The target exceeds the maximum with the entered future credits.|No se alcanza el objetivo con esos créditos y la nota máxima.|按输入学分，即使满分也无法达到目标。|入力した単位数と満点では目標に届きません。|Mit den eingegebenen Punkten liegt das Ziel über dem Maximum.
already|앞으로 0점을 받아도 목표 이상입니다.|The target remains met even with a future average of zero.|El objetivo se mantiene incluso con promedio futuro cero.|未来平均为零时仍可达到目标。|今後の平均が 0 点でも目標以上です。|Das Ziel bleibt selbst bei künftigem Durchschnitt null erreicht.
feasible|입력한 만점 범위 안의 목표입니다.|The required average is within your scale.|El promedio necesario está dentro de tu escala.|所需平均值在所设满分范围内。|必要な平均は入力した満点の範囲内です。|Der benötigte Durchschnitt liegt innerhalb der Skala.
numberError|숫자의 범위와 빈칸을 확인하세요.|Check numeric ranges and empty fields.|Revisa rangos numéricos y campos vacíos.|请检查数值范围和空白字段。|数値の範囲と空欄を確認してください。|Zahlenbereiche und leere Felder prüfen.
scaleError|환산표는 중복 없는 등급=점수 형식이어야 합니다. 점수는 0~만점, 최대 30등급입니다.|Use unique grade=points entries. Points must be 0 to maximum; up to 30 grades.|Usa nota=puntos sin duplicados, entre 0 y el máximo; hasta 30 notas.|换算表必须为不重复的等级=分数；分数介于 0 和满分之间，最多 30 项。|換算表は重複のない評価=点。点は 0～満点、最大 30 評価です。|Eindeutige Note=Punkte-Einträge, von 0 bis Maximum; höchstens 30 Noten.
courseLimit|과목은 1~100개 필요합니다.|Enter 1 to 100 courses.|Introduce de 1 a 100 asignaturas.|课程数量必须为 1 至 100。|科目数は 1～100 件です。|1 bis 100 Kurse eingeben.
nameLimit|과목명은 100자 이내로 입력하세요.|Course names are limited to 100 characters.|El nombre admite hasta 100 caracteres.|课程名最多 100 个字符。|科目名は 100 文字以内です。|Kursnamen dürfen höchstens 100 Zeichen haben.
gradeError|선택한 등급이 환산표에 없습니다. 등급을 다시 선택하세요.|A selected grade is missing from the scale. Select it again.|Una nota no está en la escala. Vuelve a elegirla.|所选等级不在换算表中，请重新选择。|選択した評価が換算表にありません。選び直してください。|Eine gewählte Note fehlt in der Tabelle. Erneut auswählen.
retakeMode|P/F 또는 제외 과목에 재수강 차감을 지정할 수 없습니다.|Retake replacement requires a graded course.|El reemplazo requiere una asignatura con nota.|P/F 或排除课程不能扣除重修旧记录。|合否科目・除外科目に再履修差し引きは指定できません。|Ersetzen ist nur bei benoteten Kursen möglich.
retakeError|재수강 차감이 이전 누적 학점·점수와 맞지 않습니다.|Replaced credits or points conflict with previous totals.|El reemplazo no concuerda con el acumulado previo.|重修扣除值与此前累计学分或分数不符。|再履修の差し引きが過去の累積値と合いません。|Ersetzte Punkte oder Noten passen nicht zu bisherigen Summen.
noGraded|평점에 반영할 누적 학점이 없습니다.|No GPA-bearing credits remain.|No quedan créditos computables.|没有可计入绩点的累计学分。|GPA 対象の累積単位がありません。|Keine benoteten Leistungspunkte vorhanden.
help1|학기 평점 = Σ(학점×환산점수) ÷ Σ학점. P/F·제외 과목은 분자·분모에 넣지 않습니다. 누적값은 이전 학점×평점에서 지정한 재수강 기록을 빼고 이번 학기 값을 더합니다.|Semester GPA = Σ(credits × points) ÷ Σcredits. Pass/fail and excluded courses enter neither sum. Cumulative totals remove specified retake records from previous credits × GPA before adding this semester.|Promedio = Σ(créditos × puntos) ÷ Σcréditos. P/F y excluidas no cuentan. El acumulado resta los registros reemplazados de los totales anteriores y añade este semestre.|学期绩点 = Σ(学分×换算分数) ÷ Σ学分。P/F 和排除课程不计分子或分母。累计值先从此前学分×绩点中扣除指定重修记录，再加入本学期成绩。|学期 GPA = Σ(単位×換算点) ÷ Σ単位。合否・除外科目は分子・分母に含めません。累積値は過去の単位×GPA から指定した再履修記録を引き、今学期を加えます。|Semesterdurchschnitt = Σ(Punkte × Notenwert) ÷ ΣPunkte. P/F und ausgeschlossene Kurse zählen nicht mit. Gesamtsummen ziehen ersetzte Einträge ab und addieren das Semester.
help2|필요 평균 = [목표×(예상 누적 학점+미래 학점)−예상 누적 총점] ÷ 미래 학점. 반올림 전 값으로 계산하고 화면은 소수 3자리입니다. 학칙·재수강 상한·졸업요건·학사경고를 판정하지 않습니다. 학점 0.1~100, 이전 누적 0~10,000, 미래 0.1~1,000, 만점 1~10. 입력은 기기에만 머무릅니다.|Required future average = [target × (projected credits + future credits) − projected quality points] ÷ future credits. Calculations use unrounded values; display uses 3 decimals. No institutional policy, retake cap, graduation or academic standing decisions. Course credits 0.1–100; previous 0–10,000; future 0.1–1,000; scale 1–10. Data stays on device.|Promedio futuro = [objetivo × (créditos acumulados previstos + futuros) − puntos acumulados] ÷ créditos futuros. Se calcula sin redondear y se muestran 3 decimales. No decide reglas académicas, límites de repetición ni graduación. Créditos por curso 0,1–100; previos 0–10.000; futuros 0,1–1.000; máximo 1–10. Datos locales.|未来所需平均 = [目标×(预计累计学分+未来学分)−预计累计加权总分] ÷ 未来学分。计算使用未舍入数值，显示三位小数。不判定校规、重修上限、毕业要求或学业警告。课程学分 0.1–100，此前累计 0–10,000，未来 0.1–1,000，满分 1–10。数据仅留本机。|必要平均 = [目標×(予想累積単位+将来単位)−予想累積総点] ÷ 将来単位。丸め前の値で計算し表示は小数 3 桁。学則・再履修上限・卒業要件・警告は判定しません。科目 0.1～100 単位、過去 0～10,000、将来 0.1～1,000、満点 1～10。データは端末内のみ。|Benötigter Durchschnitt = [Ziel × (erwartete Gesamtpunkte + künftige Punkte) − erwartete Notensumme] ÷ künftige Punkte. Ohne Zwischenrundung, Anzeige mit 3 Dezimalen. Keine Entscheidung zu Hochschulregeln, Wiederholungsgrenzen oder Abschluss. Kurs 0,1–100; bisher 0–10.000; künftig 0,1–1.000; Maximum 1–10. Daten bleiben lokal.'''
catalog={l:{} for l in langs}
for line in data.splitlines():
 key,*v=line.split('|')
 if len(v)!=6:raise ValueError((key,len(v)))
 for l,s in zip(langs,v):catalog[l][key]=s.replace('\\n','\n')
(root/'dist/locales.js').write_text(_shared_book_banner(('import {catalog as base} from "./base-locales.js";const extra='+json.dumps(catalog,ensure_ascii=False)+';export const catalog=Object.fromEntries(Object.keys(extra).map(l=>[l,{...base[l],...extra[l]}]));')),encoding='utf-8')
template='''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><base href="{base}"><title>{title}</title><link rel="stylesheet" href="style.css"></head><body><main><header><a class="brand" href="./">LOCAL / STUDY TOOLS</a><span class="badge" data-t="badge"></span><label><span data-t="language"></span> <select id="language" aria-label="{language}"><option value="ko">한국어</option><option value="en">English</option><option value="es">Español</option><option value="zh">简体中文</option><option value="ja">日本語</option><option value="de">Deutsch</option></select></label></header><section class="hero"><p class="eyebrow">SEMESTER GPA</p><h1 data-t="hero" style="white-space:pre-line"></h1><p data-t="intro"></p></section><div class="settings-grid"><section class="panel"><h2 data-t="settings"></h2><div class="fields"><label><span data-t="max"></span><input id="max" type="number" value="4.5" min="1" max="10" step="0.1"></label><label><span data-t="priorCredits"></span><input id="priorCredits" type="number" value="30" min="0" max="10000" step="0.1"></label><label><span data-t="priorGpa"></span><input id="priorGpa" type="number" value="3.2" min="0" max="10" step="0.01"></label></div><label class="field"><span data-t="scale"></span><textarea id="scale" rows="5" spellcheck="false">A+=4.5
A=4
B+=3.5
B=3
C+=2.5
C=2
D+=1.5
D=1
F=0</textarea></label><p class="footnote" data-t="scaleHint"></p></section><section class="panel"><h2 data-t="targetTitle"></h2><div class="fields"><label><span data-t="target"></span><input id="target" type="number" value="3.7" min="0" max="10" step="0.01"></label><label><span data-t="futureCredits"></span><input id="futureCredits" type="number" value="18" min="0.1" max="1000" step="0.1"></label></div><p class="footnote" data-t="help2"></p></section></div><section class="panel"><div class="result-top"><h2 data-t="courses"></h2><div class="buttons"><button id="example" data-t="example"></button><button id="add" data-t="add"></button></div></div><p class="footnote" data-t="retakeHint"></p><div class="table-wrap"><table><thead><tr><th data-t="course"></th><th data-t="credits"></th><th data-t="grade"></th><th data-t="oldCredits"></th><th data-t="oldPoints"></th><th data-t="remove"></th></tr></thead><tbody id="courses"></tbody></table></div><div class="actionbar"><button class="primary" id="calculate" data-t="calculate"></button><button id="download" disabled data-t="download"></button></div><p id="status" role="status" aria-live="polite" data-t="initial"></p></section><section class="panel"><h2 data-t="result"></h2><div class="metrics"><div><strong id="semester">—</strong><span data-t="semester"></span></div><div><strong id="cumulative">—</strong><span data-t="cumulative"></span></div><div><strong id="required">—</strong><span data-t="required"></span></div></div><p id="feasibility" role="status"></p><p id="creditSummary" class="footnote"></p></section><details><summary data-t="helpTitle"></summary><p data-t="help1"></p><p data-t="help2"></p><p><a href="https://www.itl.nist.gov/div898/software/dataplot/refman2/ch2/weigmean.pdf" target="_blank" rel="noreferrer">NIST · Weighted mean</a></p></details><footer><span data-t="footer"></span><a href="https://nanalab.kr/apps/">More Apps ↗</a></footer></main><script type="module" src="app.js"></script></body></html>'''
for lang in langs:
 out=root/'dist'/('' if lang=='ko' else lang);out.mkdir(exist_ok=True)
 html=template.replace('{lang}',lang).replace('{base}','./' if lang=='ko' else '../').replace('{title}',catalog[lang]['title']).replace('{language}',{'ko':'언어','en':'Language','es':'Idioma','zh':'语言','ja':'言語','de':'Sprache'}[lang])
 (out/'index.html').write_text(_shared_book_banner((html)),encoding='utf-8')

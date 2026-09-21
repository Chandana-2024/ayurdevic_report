import sys, copy
from pathlib import Path
sys.path[:0] = [str(Path.cwd()), str(Path('tests').resolve()), str(Path('tmp/pdf-tools').resolve())]
from test_two_report_workflow import TwoReportWorkflowTests
from src.services.report_workflow import TwoReportWorkflow
from src.services.two_report_pdf import TwoReportPDFGenerator
from pypdf import PdfReader
import pypdfium2 as pdfium
f=TwoReportWorkflowTests(); state=f._state()
state['patient_profile'].update(name='Synthetic QA Patient', age=35, gender='Female', height_cm=165, weight_kg=65, goal='Better sleep', dietary_preference='Vegetarian')
day=state['meal_plan']['days'][0]
day.pop('daily_total')
meal=day['meals'][0]
day['meals']=[{**copy.deepcopy(meal),'meal':name} for name in ('Breakfast','Lunch','Snack','Dinner')]
state['meal_plan']['days']=[{**copy.deepcopy(day),'day':i} for i in range(1,8)]
state['lifestyle_plan']={'recommendations':[{'category':'sleep','personalized_recommendation':'Synthetic doctor-reviewed sleep guidance.'}]}
g=TwoReportPDFGenerator('tmp/pdfs'); flow=TwoReportWorkflow(state)
paths=[g.generate_assessment_report(state,'steps1-9-report1.pdf')]
flow.approve(f._approval());paths.append(g.generate_final_report(state,'steps1-9-report2.pdf'))
for path in paths:
    reader=PdfReader(path); text='\n'.join(p.extract_text() for p in reader.pages)
    print(path, len(reader.pages), 'pages')
    Path(path).with_suffix('.txt').write_text(text)
    if 'report2' in path:
        for forbidden in ('failed_checks','nutrition_total','RAG','seasonal_guidance','Mid-Morning'):
            assert forbidden not in text
        assert 'APPROVE' in text
        assert 'Day 7' in text
    doc=pdfium.PdfDocument(path)
    for i,page in enumerate(doc):
        page.render(scale=1).to_pil().save(str(Path(path).with_suffix(''))+f'-{i+1}.png')

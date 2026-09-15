import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path('tests').resolve()))
sys.path.insert(0, str(Path('tmp/pdf-tools').resolve()))
from test_two_report_workflow import TwoReportWorkflowTests
from src.services.report_workflow import TwoReportWorkflow
from src.services.two_report_pdf import TwoReportPDFGenerator
from pypdf import PdfReader
import pypdfium2 as pdfium

fixtures = TwoReportWorkflowTests()
state = fixtures._state()
state['patient_profile']['name'] = 'SYNTHETIC QA FIXTURE - NOT A PATIENT'
flow = TwoReportWorkflow(state)
generator = TwoReportPDFGenerator('tmp/pdfs')
paths = [generator.generate_assessment_report(state, 'qa_assessment.pdf')]
food = state['meal_plan']['days'][0]['meals'][0]
food['foods'] *= 35
food.pop('meal_total')
state['meal_plan']['days'][0].pop('daily_total')
approval = fixtures._approval()
approval['doctor_name'] = 'SYNTHETIC TEST REVIEWER - NOT CLINICAL APPROVAL'
approval['signature'] = 'SYNTHETIC QA SIGN-OFF'
flow.approve(approval)
paths.append(generator.generate_final_report(state, 'qa_final.pdf'))
for path in paths:
    reader = PdfReader(path)
    print(path, 'pages:', len(reader.pages))
    text = '\n'.join(page.extract_text() for page in reader.pages)
    Path(path).with_suffix('.txt').write_text(text, encoding='utf-8')
    if 'assessment' in path:
        assert 'SYNTHETIC TEST REVIEWER' not in text
        assert 'PRELIMINARY AI ASSESSMENT' in text
    document = pdfium.PdfDocument(path)
    for index in range(len(document)):
        page = document[index]
        bitmap = page.render(scale=1.2)
        bitmap.to_pil().save(str(Path(path).with_suffix('')) + f'-{index + 1}.png')
        bitmap.close()
        page.close()
    document.close()

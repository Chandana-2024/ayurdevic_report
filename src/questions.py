"""Question definitions for the VedAmrit assessment workflow."""


def _prakriti_question(question_id: int, text: str, vata: str, pitta: str, kapha: str) -> dict:
    return {"id": question_id, "text": text, "options": [
        {"text": vata, "dosha": "Vata"},
        {"text": pitta, "dosha": "Pitta"},
        {"text": kapha, "dosha": "Kapha"},
    ]}


PRAKRITI_QUESTIONS = [
    _prakriti_question(1, "What is your skin usually like?", "Dry or rough skin that absorbs oil quickly.", "Soft, warm skin that may develop pigmentation, pimples, or moles.", "Oily, clear skin that absorbs oil slowly."),
    _prakriti_question(2, "What is your hair usually like?", "Dry, brittle, or rough hair that may have split ends.", "Medium-density, straight or slightly wavy hair that may gray or thin early.", "Thick, smooth hair that may be straight, wavy, or curly, with an oily scalp."),
    _prakriti_question(3, "How do you usually move?", "You move often, change position frequently, and find it hard to sit still.", "Your movements are coordinated and active.", "Your movements are calm and slow."),
    _prakriti_question(4, "How well can you continue physical activity?", "You have short bursts of energy but tire easily.", "You have strong drive and enjoy intense activity or competition.", "You have good stamina and can continue moderate activity for a long time."),
    _prakriti_question(5, "How often do you get infections, and how quickly do you recover?", "Your symptoms change or fluctuate quickly.", "You may have a strong fever or inflammation but recover quickly.", "You rarely get sick, but recovery is slow and congestion or mucus may occur."),
    _prakriti_question(6, "What is your appetite usually like?", "Your hunger changes from one meal to another.", "You have a strong appetite and may become irritable when hungry.", "You have a good appetite and can easily skip a meal."),
    _prakriti_question(7, "How much food do you usually eat at a meal?", "The amount varies, and you often prefer small portions.", "You digest food strongly and can manage larger portions.", "You digest food well, but it happens slowly and comfortably."),
    _prakriti_question(8, "How often do you feel thirsty?", "Your thirst is unpredictable, you drink in bursts, and you prefer warm drinks.", "You feel thirsty often and prefer cool drinks.", "You feel little thirst, can go a long time without drinking, and prefer warm drinks."),
    _prakriti_question(9, "How much do you usually sweat?", "You sweat little, and your sweat is usually without a strong smell.", "You sweat during exercise, and your sweat may have a noticeable smell.", "You mainly sweat during intense exercise, and your sweat is usually without a strong smell."),
    _prakriti_question(10, "How would you describe your memory and ability to remember things?", "You learn quickly but forget easily.", "You learn quickly and remember details well.", "You learn slowly but remember information for a long time."),
    _prakriti_question(11, "What is your sleep usually like?", "Your sleep is light or restless, you wake easily, and your thoughts may race.", "Your sleep is sound, but you can miss sleep when you are focused on work.", "Your sleep is deep and long, and it is difficult to give up sleep."),
    _prakriti_question(12, "How do you usually react to hot and cold temperatures?", "You prefer warmth and feel uncomfortable in the cold.", "You prefer cool surroundings and dislike too much heat or humidity.", "You prefer warmth slightly and tolerate cold fairly well."),
    _prakriti_question(13, "How do you usually begin a task or piece of work?", "You start with enthusiasm, but your motivation changes and you may lose interest.", "You are driven and goal-focused, and you take the lead.", "You start slowly and steadily and stay persistent once you begin."),
    _prakriti_question(14, "How quickly and strongly do your emotions change?", "Your emotions change often, and you become emotional or sensitive easily.", "Your emotions are strong and intense; you may become angry or frustrated.", "You are calm and stable, peaceful, content, and forgiving."),
    _prakriti_question(15, "How do you usually speak?", "You speak quickly, move between ideas, and may become distracted.", "You speak clearly, directly, sharply, and persuasively.", "You speak slowly and calmly and choose your words carefully."),
    _prakriti_question(16, "How do you usually feel and behave when competing with others?", "You dislike competition and find it stressful.", "You enjoy competition and perform well under pressure.", "You handle competition calmly and remain steady under pressure."),
    _prakriti_question(17, "What are your bowel movements usually like?", "They are irregular, with constipation, gas or bloating, and hard or dry stools.", "They are regular and frequent, but stools may sometimes be loose.", "They are slow and easy; stools may be heavy, sticky, and well formed."),
    _prakriti_question(18, "How easily do you usually lose weight?", "You lose weight easily.", "You can lose weight with focused diet and exercise.", "You need consistent effort, and weight loss is slower."),
    _prakriti_question(19, "What is your mind usually like during the day?", "Your mind is restless, easily distracted, and very active.", "Your mind is focused and sharp but may become agitated.", "Your mind is relaxed and unhurried, and you are not easily pressured."),
    _prakriti_question(20, "How would you describe your usual emotional nature?", "You may feel anxious or sensitive, and your emotions may be unpredictable.", "You may become angry or agitated quickly and have intense emotions.", "You are calm and slow to anger, but emotional detachment may be difficult."),
    _prakriti_question(21, "What tastes and types of food do you usually prefer?", "You prefer sweet, sour, salty, spicy, or hot foods and drinks.", "You prefer sour, salty, spicy, and strong flavors, along with cool drinks.", "You prefer sweet, salty, and calorie-rich foods, along with warm or sweet drinks."),
]


def _vikriti_question(question_id: str, dosha: str, text: str) -> dict:
    return {"id": question_id, "dosha": dosha, "text": text, "options": {
        "1": {"text": "Not at all", "score": 1},
        "2": {"text": "Somewhat / Occasionally", "score": 3},
        "3": {"text": "Very often", "score": 5},
    }}


VIKRITI_QUESTIONS = [
    _vikriti_question("V1", "Vata", "Recently, have you had trouble concentrating, felt mentally scattered or overwhelmed, worried excessively, or felt restless?"),
    _vikriti_question("V2", "Vata", "Recently, have you had trouble falling or staying asleep, making decisions, finishing tasks, or keeping commitments?"),
    _vikriti_question("V3", "Vata", "Recently, have you become more forgetful, acted impulsively or inconsistently, or struggled to follow a regular routine?"),
    _vikriti_question("V4", "Vata", "Recently, have you had a lasting dry cough, often needed to clear your throat, had repeated throat or voice problems, or found it hard to express yourself?"),
    _vikriti_question("V5", "Vata", "Recently, have you had gas, stomach cramps or bloating after meals, an irregular appetite, or trouble digesting and passing food?"),
    _vikriti_question("V6", "Vata", "Recently, have you had constipation, trouble passing urine, or changes in menstrual or sexual function?"),
    _vikriti_question("V7", "Vata", "Recently, have you felt dizzy when standing, had unusually cold hands or feet, or felt your heart beating unusually fast or strongly?"),
    _vikriti_question("P1", "Pitta", "Recently, have you felt irritable, impatient, easily frustrated, angry, or aggressive toward other people?"),
    _vikriti_question("P2", "Pitta", "Recently, have you been unusually critical or judgmental, jealous, very competitive, or very strong in your opinions?"),
    _vikriti_question("P3", "Pitta", "Recently, have you found it hard to stop working, felt driven to achieve, or repeatedly thought about past situations?"),
    _vikriti_question("P4", "Pitta", "Recently, have you noticed worsening eyesight, headaches with sensitivity to light or visual changes, or itchy, sensitive, or watery eyes?"),
    _vikriti_question("P5", "Pitta", "Recently, have you had an unusually strong appetite or bowel movements more often than usual?"),
    _vikriti_question("P6", "Pitta", "Recently, have you had acid reflux, heartburn, ulcer symptoms, or stomach discomfort after eating fatty food?"),
    _vikriti_question("P7", "Pitta", "Recently, have you had liver problems, inflammatory skin conditions, or skin that stays itchy or irritated?"),
    _vikriti_question("K1", "Kapha", "Recently, have you withdrawn during conflicts, resisted changes to your routine, or found it difficult to move on from people or past situations?"),
    _vikriti_question("K2", "Kapha", "Recently, have you had short-term memory problems, found it hard to get started in the morning, or struggled to take action even when you planned to?"),
    _vikriti_question("K3", "Kapha", "Recently, have you eaten more because of your emotions rather than hunger, or felt less confident about handling challenges?"),
    _vikriti_question("K4", "Kapha", "Recently, have you noticed reduced taste or smell, a dry mouth, or repeated mouth sores?"),
    _vikriti_question("K5", "Kapha", "Recently, have you felt nauseated after eating, remained full for a long time, or felt sleepy or heavy after meals?"),
    _vikriti_question("K6", "Kapha", "Recently, have you had difficult breathing, heaviness in the chest, wheezing or asthma episodes, or repeated chest colds or a wet cough?"),
    _vikriti_question("K7", "Kapha", "Recently, have you had stiffness that limits movement, stiff or swollen knees, or swollen fingers?"),
]


def _agni_question(question_id: str, question: str, options: list[tuple[str, str, int]]) -> dict:
    return {"id": question_id, "question": question, "options": [
        {"text": text, "agni_state": agni_state, "score": score}
        for text, agni_state, score in options
    ]}


AGNI_QUESTIONS = [
    _agni_question("A1", "Which option best describes how well you digest food?", [("You cannot digest even small amounts of food", "Mandagni", 1), ("Your ability to digest food changes; sometimes you can and sometimes you cannot", "Vishamagni", 2), ("You can digest almost all foods when you eat the right amount", "Samagni", 3), ("You can digest almost any food easily, even large amounts", "Tikshnagni", 4)]),
    _agni_question("A2", "How long after a meal does it usually take before you feel hungry again?", [("About 8 hours", "Mandagni", 1), ("The timing is not consistent", "Vishamagni", 2), ("6 to 8 hours", "Samagni", 3), ("Less than 6 hours", "Tikshnagni", 4)]),
    _agni_question("A3", "How does your digestion change when your routine is disturbed, such as by irregular meals, poor sleep, or emotional stress?", [("Your digestion is disturbed by even a small change", "Mandagni", 1), ("Your digestion is disturbed by major changes", "Vishamagni", 2), ("Your digestion is not affected much", "Samagni", 3), ("Your digestion is disturbed at first but adjusts later", "Tikshnagni", 4)]),
    _agni_question("A4", "How many meals do you usually eat each day?", [("Fewer than 2 meals a day", "Mandagni", 1), ("The number changes between 1 and 4 meals a day", "Vishamagni", 2), ("Usually 2 to 3 meals a day", "Samagni", 3), ("Almost always more than 3 meals a day", "Tikshnagni", 4)]),
    _agni_question("A5", "How long can you usually wait after you feel hungry before eating?", [("More than 2 hours", "Mandagni", 1), ("Sometimes up to 1 hour, but sometimes less than 1 hour", "Vishamagni", 2), ("About 1 to 2 hours", "Samagni", 3), ("It is very difficult to wait when hungry", "Tikshnagni", 4)]),
    _agni_question("A6", "How much food do you usually eat at each meal?", [("Usually small meals", "Mandagni", 1), ("Sometimes large and sometimes small meals", "Vishamagni", 2), ("Neither very small nor very large meals", "Samagni", 3), ("Usually large meals", "Tikshnagni", 4)]),
    _agni_question("A7", "How long does it usually take you to digest a heavy meal?", [("Usually longer than normal", "Mandagni", 1), ("The time varies", "Vishamagni", 2), ("A normal amount of time", "Samagni", 3), ("Quite quickly", "Tikshnagni", 4)]),
    _agni_question("A8", "What are your bowel habits usually like?", [("You tend to have constipation", "Mandagni", 1), ("Your stools are sometimes hard and sometimes soft", "Vishamagni", 2), ("Your stools are normal, neither hard nor soft", "Samagni", 3)]),
    _agni_question("A9", "How regular are your usual meal times?", [("You usually eat after the scheduled time", "Mandagni", 1), ("You usually eat before or after the scheduled time", "Vishamagni", 2), ("You usually eat exactly at the scheduled time", "Samagni", 3), ("You usually eat before the scheduled time", "Tikshnagni", 4)]),
    _agni_question("A10", "How do you usually feel after your food has been fully digested?", [("You often feel heaviness in your abdomen or body", "Mandagni", 1), ("You sometimes feel slight heaviness", "Vishamagni", 2), ("You mostly feel light", "Samagni", 3), ("You feel light quite soon after eating", "Tikshnagni", 4)]),
    _agni_question("A11", "What do you usually feel when you see foods that you like?", [("You do not want to eat even when hungry", "Mandagni", 1), ("Sometimes you want to eat and sometimes you do not", "Vishamagni", 2), ("You want to eat the food", "Samagni", 3), ("You want to eat almost any food, whether you like it or not", "Tikshnagni", 4)]),
]


QUESTIONS = PRAKRITI_QUESTIONS


_PRAKRITI_HINDI = {
    1: ("आपकी त्वचा आमतौर पर कैसी रहती है?", ["रूखी या खुरदरी त्वचा, जो तेल जल्दी सोख लेती है।", "नरम, गर्म त्वचा, जिसमें झाइयां, मुंहासे या तिल हो सकते हैं।", "तैलीय और साफ त्वचा, जो तेल धीरे-धीरे सोखती है।"]),
    2: ("आपके बाल आमतौर पर कैसे रहते हैं?", ["रूखे, कमजोर या खुरदरे बाल, जिनमें दोमुंहे सिरे हो सकते हैं।", "मध्यम घनत्व वाले, सीधे या थोड़े लहरदार बाल, जिनमें जल्दी सफेद होने या पतले होने की प्रवृत्ति हो सकती है।", "घने और मुलायम बाल, जो सीधे, लहरदार या घुंघराले हो सकते हैं; सिर की त्वचा तैलीय रहती है।"]),
    3: ("आप आमतौर पर कैसे चलते-फिरते हैं?", ["आप बार-बार हिलते-डुलते हैं, स्थिति बदलते हैं और स्थिर बैठना कठिन लगता है।", "आपकी गतिविधियां संतुलित और सक्रिय रहती हैं।", "आपकी गतिविधियां शांत और धीमी रहती हैं।"]),
    4: ("आप कितनी देर तक शारीरिक गतिविधि जारी रख सकते हैं?", ["आपमें थोड़ी देर के लिए ऊर्जा अधिक रहती है, लेकिन आप जल्दी थक जाते हैं।", "आपमें मजबूत उत्साह होता है और आप कठिन गतिविधि या प्रतियोगिता पसंद करते हैं।", "आपकी सहनशक्ति अच्छी होती है और आप लंबे समय तक मध्यम गतिविधि कर सकते हैं।"]),
    5: ("आपको संक्रमण कितनी बार होता है और आप कितनी जल्दी ठीक होते हैं?", ["आपके लक्षण जल्दी-जल्दी बदलते रहते हैं।", "आपको तेज बुखार या सूजन हो सकती है, लेकिन आप जल्दी ठीक हो जाते हैं।", "आप कम बीमार पड़ते हैं, लेकिन ठीक होने में समय लगता है और नाक बंद या बलगम हो सकता है।"]),
    6: ("आपकी भूख आमतौर पर कैसी रहती है?", ["आपकी भूख एक भोजन से दूसरे भोजन तक बदलती रहती है।", "आपको तेज भूख लगती है और भूख लगने पर चिड़चिड़ापन हो सकता है।", "आपकी भूख अच्छी रहती है और आप आसानी से एक भोजन छोड़ सकते हैं।"]),
    7: ("आप एक बार में आमतौर पर कितना भोजन करते हैं?", ["मात्रा बदलती रहती है और आप अक्सर कम मात्रा पसंद करते हैं।", "आपका पाचन अच्छा रहता है और आप अधिक मात्रा संभाल सकते हैं।", "आपका पाचन अच्छा रहता है, लेकिन भोजन धीरे-धीरे और आराम से पचता है।"]),
    8: ("आपको आमतौर पर कितनी बार प्यास लगती है?", ["प्यास का कोई निश्चित समय नहीं होता, आप थोड़ी-थोड़ी देर में पीते हैं और गर्म पेय पसंद करते हैं।", "आपको बार-बार प्यास लगती है और आप ठंडे पेय पसंद करते हैं।", "आपको कम प्यास लगती है, आप लंबे समय तक बिना पानी के रह सकते हैं और गर्म पेय पसंद करते हैं।"]),
    9: ("आपको आमतौर पर कितना पसीना आता है?", ["आपको कम पसीना आता है और उसमें आमतौर पर तेज गंध नहीं होती।", "व्यायाम के दौरान पसीना आता है और उसमें तेज गंध हो सकती है।", "मुख्य रूप से कठिन व्यायाम के दौरान पसीना आता है और उसमें आमतौर पर तेज गंध नहीं होती।"]),
    10: ("आपकी याददाश्त और चीजें याद रखने की क्षमता कैसी है?", ["आप जल्दी सीखते हैं, लेकिन जल्दी भूल भी जाते हैं।", "आप जल्दी सीखते हैं और बातें अच्छी तरह याद रखते हैं।", "आप धीरे सीखते हैं, लेकिन बातें लंबे समय तक याद रखते हैं।"]),
    11: ("आपकी नींद आमतौर पर कैसी रहती है?", ["आपकी नींद हल्की या बेचैन रहती है, आप जल्दी जाग जाते हैं और विचार चलते रहते हैं।", "आपकी नींद अच्छी रहती है, लेकिन काम में व्यस्त होने पर आप नींद कम कर सकते हैं।", "आपकी नींद गहरी और लंबी रहती है और नींद छोड़ना कठिन लगता है।"]),
    12: ("आप गर्मी और ठंडे तापमान पर आमतौर पर कैसी प्रतिक्रिया देते हैं?", ["आप गर्मी पसंद करते हैं और ठंड में असहज महसूस करते हैं।", "आप ठंडा वातावरण पसंद करते हैं और बहुत अधिक गर्मी या नमी पसंद नहीं करते।", "आपको थोड़ी गर्मी पसंद है और आप ठंड को काफी अच्छी तरह सहन कर लेते हैं।"]),
    13: ("आप किसी काम या कार्य की शुरुआत आमतौर पर कैसे करते हैं?", ["आप उत्साह से शुरू करते हैं, लेकिन रुचि या प्रेरणा बदल सकती है।", "आप लक्ष्य पर केंद्रित रहते हैं, प्रेरित होते हैं और नेतृत्व करते हैं।", "आप धीरे-धीरे शुरू करते हैं और शुरू करने के बाद लगातार लगे रहते हैं।"]),
    14: ("आपकी भावनाएं कितनी जल्दी और कितनी तीव्रता से बदलती हैं?", ["आपकी भावनाएं बार-बार बदलती हैं और आप जल्दी भावुक या संवेदनशील हो जाते हैं।", "आपकी भावनाएं मजबूत और तीव्र होती हैं; आपको गुस्सा या निराशा हो सकती है।", "आप शांत और स्थिर रहते हैं तथा संतुष्ट और क्षमाशील होते हैं।"]),
    15: ("आप आमतौर पर कैसे बोलते हैं?", ["आप जल्दी बोलते हैं, बातों के बीच तेजी से बदलते हैं और ध्यान भटक सकता है।", "आप स्पष्ट, सीधे, प्रभावशाली और समझाने वाले तरीके से बोलते हैं।", "आप धीरे और शांत बोलते हैं तथा शब्द सोच-समझकर चुनते हैं।"]),
    16: ("दूसरों के साथ प्रतियोगिता करते समय आप कैसा महसूस और व्यवहार करते हैं?", ["आप प्रतियोगिता पसंद नहीं करते और उसे तनावपूर्ण पाते हैं।", "आप प्रतियोगिता पसंद करते हैं और दबाव में अच्छा प्रदर्शन करते हैं।", "आप प्रतियोगिता को शांति से संभालते हैं और दबाव में स्थिर रहते हैं।"]),
    17: ("आपका मल त्याग आमतौर पर कैसा रहता है?", ["यह अनियमित रहता है, कब्ज, गैस या पेट फूलना तथा कड़ा या सूखा मल हो सकता है।", "यह नियमित और बार-बार होता है, लेकिन मल कभी-कभी पतला हो सकता है।", "यह धीमा और आसानी से होता है; मल भारी, चिपचिपा और अच्छी तरह बना हुआ हो सकता है।"]),
    18: ("आपका वजन आमतौर पर कितनी आसानी से कम होता है?", ["आपका वजन आसानी से कम हो जाता है।", "खान-पान और व्यायाम पर ध्यान देने से आपका वजन कम हो सकता है।", "आपको लगातार प्रयास करना पड़ता है और वजन धीरे कम होता है।"]),
    19: ("दिन के समय आपका मन आमतौर पर कैसा रहता है?", ["मन बेचैन और बहुत सक्रिय रहता है तथा ध्यान आसानी से भटकता है।", "मन एकाग्र और तेज रहता है, लेकिन कभी-कभी उत्तेजित हो सकता है।", "मन शांत और धीमा रहता है तथा आप पर दबाव का असर आसानी से नहीं होता।"]),
    20: ("आप अपने सामान्य भावनात्मक स्वभाव का वर्णन कैसे करेंगे?", ["आप चिंतित या संवेदनशील हो सकते हैं और भावनाएं अनिश्चित हो सकती हैं।", "आप जल्दी गुस्सा या उत्तेजित हो सकते हैं और भावनाएं तीव्र होती हैं।", "आप शांत रहते हैं और जल्दी गुस्सा नहीं होते, लेकिन भावनात्मक दूरी बनाना कठिन हो सकता है।"]),
    21: ("आपको आमतौर पर कौन-से स्वाद और किस प्रकार का भोजन पसंद है?", ["आपको मीठा, खट्टा, नमकीन, मसालेदार या गर्म भोजन और पेय पसंद हैं।", "आपको खट्टे, नमकीन, मसालेदार और तेज स्वाद पसंद हैं तथा ठंडे पेय पसंद हैं।", "आपको मीठा, नमकीन और अधिक कैलोरी वाला भोजन तथा गर्म या मीठे पेय पसंद हैं।"]),
}

for question in PRAKRITI_QUESTIONS:
    question["text_hi"], option_texts = _PRAKRITI_HINDI[question["id"]]
    for option, text_hi in zip(question["options"], option_texts):
        option["text_hi"] = text_hi


_VIKRITI_HINDI = {
    "V1": "हाल ही में, क्या आपको ध्यान लगाने में परेशानी, मन बिखरा या बोझिल लगना, बहुत अधिक चिंता या बेचैनी महसूस हुई है?",
    "V2": "हाल ही में, क्या आपको सोने या सोते रहने, निर्णय लेने, काम पूरा करने या अपनी जिम्मेदारियां निभाने में परेशानी हुई है?",
    "V3": "हाल ही में, क्या आप अधिक भूलने लगे हैं, आपका व्यवहार अचानक या अस्थिर हुआ है, या नियमित दिनचर्या बनाए रखना कठिन लगा है?",
    "V4": "हाल ही में, क्या आपको लगातार सूखी खांसी, बार-बार गला साफ करने की जरूरत, गले या आवाज की समस्या, या अपनी बात कहने में कठिनाई हुई है?",
    "V5": "हाल ही में, क्या आपको गैस, भोजन के बाद पेट में ऐंठन या फूलना, अनियमित भूख, या भोजन पचाने और आगे बढ़ाने में परेशानी हुई है?",
    "V6": "हाल ही में, क्या आपको कब्ज, पेशाब करने में परेशानी, या मासिक धर्म या यौन कार्य में बदलाव हुआ है?",
    "V7": "हाल ही में, क्या खड़े होने पर चक्कर, हाथ-पैर असामान्य रूप से ठंडे, या दिल की धड़कन तेज या जोर से महसूस हुई है?",
    "P1": "हाल ही में, क्या आप चिड़चिड़े, अधीर, जल्दी निराश, गुस्सैल या दूसरों के प्रति आक्रामक महसूस कर रहे हैं?",
    "P2": "हाल ही में, क्या आप असामान्य रूप से आलोचनात्मक या दूसरों को आंकने वाले, ईर्ष्यालु, बहुत प्रतिस्पर्धी या अपनी राय पर बहुत अड़े हुए हैं?",
    "P3": "हाल ही में, क्या काम शुरू करने के बाद रुकना कठिन लगा, सफलता पाने की तीव्र इच्छा रही, या पुरानी घटनाओं के बारे में बार-बार सोचते रहे?",
    "P4": "हाल ही में, क्या नजर कमजोर हुई, रोशनी से संवेदनशीलता या दृश्य बदलाव के साथ सिरदर्द हुआ, या आंखों में खुजली, संवेदनशीलता या पानी आया है?",
    "P5": "हाल ही में, क्या आपको बहुत तेज भूख लगी है या सामान्य से अधिक बार मल त्याग हुआ है?",
    "P6": "हाल ही में, क्या आपको एसिड रिफ्लक्स, सीने में जलन, अल्सर के लक्षण, या तैलीय भोजन के बाद पेट में परेशानी हुई है?",
    "P7": "हाल ही में, क्या आपको लीवर की समस्या, सूजन वाली त्वचा की समस्या, या लगातार खुजली या जलन वाली त्वचा हुई है?",
    "K1": "हाल ही में, क्या आप विवाद के समय अलग हो जाते हैं, दिनचर्या में बदलाव का विरोध करते हैं, या लोगों और पुरानी परिस्थितियों से आगे बढ़ना कठिन पाते हैं?",
    "K2": "हाल ही में, क्या आपको हाल की बातें याद रखने में परेशानी, सुबह शुरू होने में कठिनाई, या योजना होने पर भी काम करने में परेशानी हुई है?",
    "K3": "हाल ही में, क्या आपने भूख के बजाय भावनाओं के कारण अधिक खाया है, या चुनौतियों का सामना करने के अपने आत्मविश्वास में कमी महसूस की है?",
    "K4": "हाल ही में, क्या स्वाद या गंध कम महसूस हुई, मुंह सूखा रहा, या बार-बार मुंह में छाले हुए हैं?",
    "K5": "हाल ही में, क्या भोजन के बाद जी मिचलाया, लंबे समय तक पेट भरा रहा, या नींद और भारीपन महसूस हुआ है?",
    "K6": "हाल ही में, क्या सांस लेने में परेशानी, सीने में भारीपन, घरघराहट या अस्थमा, या बार-बार जुकाम या बलगम वाली खांसी हुई है?",
    "K7": "हाल ही में, क्या ऐसी अकड़न हुई जिससे चलना-फिरना सीमित हो, घुटने अकड़े या सूजे हों, या उंगलियों में सूजन हुई हो?",
}

for question in VIKRITI_QUESTIONS:
    question["text_hi"] = _VIKRITI_HINDI[question["id"]]
    for option in question["options"].values():
        option["text_hi"] = {1: "बिल्कुल नहीं", 3: "कुछ हद तक / कभी-कभी", 5: "बहुत बार"}[option["score"]]


_AGNI_HINDI = {
    "A1": ("भोजन को पचाने की आपकी क्षमता का सबसे अच्छा वर्णन कौन-सा विकल्प करता है?", ["थोड़ी मात्रा में भी भोजन पचाना कठिन होता है", "पाचन क्षमता बदलती रहती है; कभी भोजन पचता है और कभी नहीं", "सही मात्रा में खाने पर लगभग सभी भोजन पच जाते हैं", "बड़ी मात्रा में भी लगभग हर भोजन आसानी से पच जाता है"]),
    "A2": ("भोजन के बाद आमतौर पर कितनी देर में आपको फिर भूख लगती है?", ["लगभग 8 घंटे बाद", "समय निश्चित नहीं रहता", "6 से 8 घंटे बाद", "6 घंटे से पहले"]),
    "A3": ("अनियमित भोजन, खराब नींद या भावनात्मक तनाव से दिनचर्या बिगड़ने पर आपका पाचन कैसे बदलता है?", ["थोड़े से बदलाव से भी पाचन बिगड़ जाता है", "बड़े बदलाव से पाचन बिगड़ जाता है", "पाचन पर अधिक असर नहीं पड़ता", "शुरू में पाचन बिगड़ता है, फिर शरीर अनुकूल हो जाता है"]),
    "A4": ("आप आमतौर पर हर दिन कितनी बार भोजन करते हैं?", ["दिन में 2 बार से कम", "दिन में 1 से 4 बार, संख्या बदलती रहती है", "आमतौर पर दिन में 2 से 3 बार", "लगभग हमेशा दिन में 3 बार से अधिक"]),
    "A5": ("भूख लगने के बाद आप आमतौर पर भोजन किए बिना कितनी देर रह सकते हैं?", ["2 घंटे से अधिक", "कभी 1 घंटे तक, लेकिन कभी 1 घंटे से कम", "लगभग 1 से 2 घंटे", "भूख लगने पर इंतजार करना बहुत कठिन होता है"]),
    "A6": ("आप हर भोजन में आमतौर पर कितना खाना खाते हैं?", ["आमतौर पर कम मात्रा में", "कभी अधिक और कभी कम मात्रा में", "न बहुत कम और न बहुत अधिक", "आमतौर पर अधिक मात्रा में"]),
    "A7": ("भारी भोजन को पचाने में आपको आमतौर पर कितना समय लगता है?", ["आमतौर पर सामान्य से अधिक समय", "समय बदलता रहता है", "सामान्य समय", "काफी जल्दी"]),
    "A8": ("आपकी मल त्याग की आदतें आमतौर पर कैसी रहती हैं?", ["कब्ज की प्रवृत्ति रहती है", "मल कभी कड़ा और कभी नरम रहता है", "मल सामान्य रहता है, न कड़ा न नरम"]),
    "A9": ("आपके भोजन का समय आमतौर पर कितना नियमित रहता है?", ["आप आमतौर पर तय समय के बाद खाते हैं", "आप तय समय से पहले या बाद में खाते हैं", "आप आमतौर पर तय समय पर ही खाते हैं", "आप आमतौर पर तय समय से पहले खाते हैं"]),
    "A10": ("भोजन पूरी तरह पचने के बाद आपको आमतौर पर कैसा महसूस होता है?", ["पेट या शरीर में अक्सर भारीपन लगता है", "कभी-कभी हल्का भारीपन लगता है", "अधिकतर हल्कापन महसूस होता है", "भोजन के थोड़ी देर बाद ही हल्कापन महसूस होता है"]),
    "A11": ("अपने पसंदीदा भोजन को देखकर आपको आमतौर पर कैसा महसूस होता है?", ["भूख लगने पर भी खाने की इच्छा नहीं होती", "कभी खाने की इच्छा होती है और कभी नहीं", "खाना खाने की इच्छा होती है", "पसंद हो या न हो, लगभग हर भोजन खाने की इच्छा होती है"]),
}

for question in AGNI_QUESTIONS:
    question["question_hi"], option_texts = _AGNI_HINDI[question["id"]]
    for option, text_hi in zip(question["options"], option_texts):
        option["text_hi"] = text_hi

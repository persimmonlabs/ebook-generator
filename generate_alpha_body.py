#!/usr/bin/env python3
"""
Generate ALPHA BODY PROTOCOL seed file without using LLM.
Manually structured content with deterministic HTML generation.
"""

import uuid
from datetime import datetime
from pathlib import Path
from html_builder import build_html


def generate_seed():
    """Generate the complete seed file for ALPHA BODY PROTOCOL."""

    ebook_id = str(uuid.uuid4())

    # Ebook metadata
    ebook = {
        "id": ebook_id,
        "title_en": "ALPHA BODY PROTOCOL",
        "title_pt": "ALPHA BODY PROTOCOL",
        "slug": "alpha-body-protocol",
        "description_en": "The simple manual for building a respectable body without the bullshit. A brutally efficient operating manual for the male body, designed to build strength, health, and self-confidence.",
        "description_pt": "O manual simples para construir um corpo respeitável sem frescura. Um manual de operações brutalmente eficiente para o corpo masculino, projetado para construir força, saúde e autoconfiança.",
        "cover_image_url": "images/cover.png",
        "price_usd": 1997,
        "price_brl": 9970,
        "status": "draft",
    }

    # Define all chapters with their content blocks
    chapters = [
        create_introduction(),
        create_chapter_1(),
        create_chapter_2(),
        create_chapter_3(),
        create_chapter_4(),
        create_chapter_5(),
        create_chapter_6(),
        create_chapter_7(),
        create_conclusion(),
        create_resources(),
    ]

    # Build HTML for each chapter
    for ch in chapters:
        ch["content_en"] = build_html(ch["blocks_en"])
        ch["content_pt"] = build_html(ch["blocks_pt"])
        ch["ebook_id"] = ebook_id
        # Estimate read time (roughly 200 words per minute)
        word_count = len(ch["content_en"].split())
        ch["estimated_read_time_minutes"] = max(1, word_count // 200)

    # Calculate total read time
    total_time = sum(ch["estimated_read_time_minutes"] for ch in chapters)

    # Generate SQL
    sql = generate_sql(ebook, chapters, total_time)

    # Save to file
    output_dir = Path("output") / f"{datetime.now().strftime('%Y-%m-%d')}_alpha-body-protocol"
    output_dir.mkdir(parents=True, exist_ok=True)

    seed_file = output_dir / "seed.sql"
    seed_file.write_text(sql, encoding="utf-8")

    # Generate image prompts file
    image_prompts = generate_image_prompts(chapters)
    prompts_file = output_dir / "image_prompts.txt"
    prompts_file.write_text(image_prompts, encoding="utf-8")

    print(f"Generated seed file: {seed_file}")
    print(f"Generated image prompts: {prompts_file}")
    print(f"Total chapters: {len(chapters)}")
    print(f"Total read time: ~{total_time} minutes")

    return seed_file


def create_introduction():
    """Create Introduction chapter."""
    blocks_en = [
        {"type": "heading", "level": 2, "text": "Why This Protocol Exists"},
        {"type": "paragraph", "text": "We live in an era of information overload and a lack of clarity. The fitness industry, in particular, has become a swamp of contradictory advice, miracle products, and impractical routines that do more to sell supplements and gym memberships than to build strong, respectable bodies. The result is a legion of frustrated men who invest time and money without achieving the results they desire."},
        {"type": "paragraph", "text": "The ALPHA BODY PROTOCOL was born from the need for a return to fundamental principles. This is not a \"fitness\" program. It is an operating manual for the male body, designed to be brutally efficient and straight to the point. The goal is not to turn you into a competitive bodybuilder, but into a man who projects strength, health, and self-confidence in all areas of his life. It's about building a body that functions as a social weapon: a tool that commands respect before you even say a word."},

        {"type": "heading", "level": 2, "text": "The Problem with the Modern Fitness Industry"},
        {"type": "paragraph", "text": "The conventional approach fails for three main reasons:"},
        {"type": "list", "ordered": True, "items": [
            "Unnecessary complexity creates paralysis. Six-day-a-week workout routines, diets that require weighing every gram of broccoli, and an endless list of expensive supplements make consistency nearly impossible for the average man with real responsibilities.",
            "The focus on irrelevant metrics leads to burnout and injuries. The obsession with minimal body fat percentages, the pursuit of a \"six-pack\" at all costs, or lifting dangerous loads to inflate the ego result, ironically, in a less healthy and imposing appearance.",
            "Ignorance of the invisible pillars sabotages results. Most programs focus exclusively on training and diet, neglecting the true result multipliers: hormonal optimization, sleep quality, and posture."
        ]},

        {"type": "heading", "level": 2, "text": "What You Will Learn"},
        {"type": "paragraph", "text": "This manual is an integrated system. Each chapter builds on the previous one to create a synergistic effect. You will learn to:"},
        {"type": "list", "ordered": False, "items": [
            "Train minimally and effectively with a 3-4 day-a-week plan, focused on compound movements that build strength and muscle mass symmetrically and functionally.",
            "Master a protein-centric, nutrient-dense nutritional approach that allows for flexibility and sustainable results without obsessive calorie counting.",
            "Discover how to optimize your hormones naturally, managing testosterone, cortisol, and other key hormones to maximize masculinity, energy, and fat burning.",
            "Turn your sleep into an anabolic tool to accelerate muscle recovery and mental clarity.",
            "Learn to project power through posture, correcting postural imbalances to create a physical presence of authority and confidence."
        ]},

        {"type": "heading", "level": 2, "text": "How to Use This Manual"},
        {"type": "paragraph", "text": "Read this ebook from start to finish once to understand the philosophy behind the protocol. Then, use the chapters as a reference to implement each component in your life. Don't try to change everything overnight. Start with the training, then adjust your nutrition, and then optimize the other pillars."},
        {"type": "callout", "style": "tip", "title": "Key Principle", "content": "The ALPHA BODY PROTOCOL is not a quick fix. It is a set of lifelong principles. The goal is simplicity, consistency, and building a body that serves you, not the other way around."},
    ]

    blocks_pt = [
        {"type": "heading", "level": 2, "text": "Por que este protocolo existe"},
        {"type": "paragraph", "text": "Vivemos em uma era de excesso de informação e falta de clareza. A indústria de fitness, em particular, tornou-se um pântano de conselhos contraditórios, produtos milagrosos e rotinas impraticáveis que servem mais para vender suplementos e assinaturas de academia do que para construir corpos fortes e respeitáveis. O resultado é uma legião de homens frustrados, que investem tempo e dinheiro sem obter os resultados que desejam."},
        {"type": "paragraph", "text": "O ALPHA BODY PROTOCOL nasceu da necessidade de um retorno aos princípios fundamentais. Este não é um programa de \"fitness\". É um manual de operações para o corpo masculino, desenhado para ser brutalmente eficiente e direto ao ponto. O objetivo não é transformá-lo em um fisiculturista de competição, mas sim em um homem que projeta força, saúde e autoconfiança em todas as áreas da sua vida."},

        {"type": "heading", "level": 2, "text": "O problema com a indústria fitness moderna"},
        {"type": "paragraph", "text": "A abordagem convencional falha por três motivos principais:"},
        {"type": "list", "ordered": True, "items": [
            "A complexidade desnecessária cria paralisia. Rotinas de treino de seis dias por semana, dietas que exigem pesar cada grama de brócolis e uma lista interminável de suplementos caros tornam a consistência quase impossível.",
            "O foco em métricas irrelevantes leva ao esgotamento e lesões. A obsessão por percentuais de gordura corporal mínimos resulta em uma aparência menos saudável e imponente.",
            "A ignorância dos pilares invisíveis sabota os resultados. A maioria dos programas foca exclusivamente em treino e dieta, negligenciando os verdadeiros multiplicadores de resultados."
        ]},

        {"type": "heading", "level": 2, "text": "O que você vai aprender"},
        {"type": "paragraph", "text": "Este manual é um sistema integrado. Cada capítulo se baseia no anterior para criar um efeito sinérgico. Você aprenderá a:"},
        {"type": "list", "ordered": False, "items": [
            "Treinar de forma minimalista e eficaz com um plano de 3 a 4 dias por semana.",
            "Dominar uma abordagem nutricional centrada em proteína e densidade nutricional.",
            "Descobrir como otimizar seus hormônios naturalmente.",
            "Transformar seu sono em uma ferramenta anabólica.",
            "Projetar poder através da postura."
        ]},

        {"type": "heading", "level": 2, "text": "Como usar este manual"},
        {"type": "paragraph", "text": "Leia este ebook do início ao fim uma vez para entender a filosofia por trás do protocolo. Em seguida, use os capítulos como referência para implementar cada componente em sua vida."},
        {"type": "callout", "style": "tip", "title": "Princípio Chave", "content": "O ALPHA BODY PROTOCOL não é uma solução rápida. É um conjunto de princípios para toda a vida. O objetivo é a simplicidade, a consistência e a construção de um corpo que sirva a você."},
    ]

    return {
        "chapter_number": 1,
        "title_en": "Introduction",
        "title_pt": "Introdução",
        "slug": "introduction",
        "summary_en": "Why this protocol exists, the problem with modern fitness, and how to use this manual for maximum results.",
        "summary_pt": "Por que este protocolo existe, o problema com o fitness moderno e como usar este manual para resultados máximos.",
        "blocks_en": blocks_en,
        "blocks_pt": blocks_pt,
        "cover_image_url": "images/chapter_1.png",
        "is_free_preview": True,
        "is_published": False,
    }


def create_chapter_1():
    """Create Chapter 1: The Body as a Social Weapon."""
    blocks_en = [
        {"type": "heading", "level": 2, "text": "1.1 The Brutal Reality: First Impressions are Physical"},
        {"type": "paragraph", "text": "Let's be direct: the world judges by appearances. Before you open your mouth to demonstrate your intelligence, character, or status, the people around you have already formed an opinion based on your physical presence. This is an inconvenient truth, often ignored in politically correct discourse, but deeply rooted in our evolutionary biology."},
        {"type": "paragraph", "text": "A man with broad shoulders, an upright posture, and a firm handshake communicates competence and control without saying a single word. He takes up space. He projects authority. In contrast, a man with slumped shoulders and a hunched posture communicates submission and passivity, regardless of his qualifications."},
        {"type": "callout", "style": "warning", "title": "Reality Check", "content": "Denying this reality doesn't make it any less true. The only logical response is to use it to your advantage."},

        {"type": "heading", "level": 2, "text": "1.2 Respect, Authority, and Presence"},
        {"type": "paragraph", "text": "Respect is not something you ask for; it's something you command. Your physical presence is the first line of that command. Authority is not just about the title you hold; it's about the aura you exude. A strong, healthy body is the foundation of that aura."},
        {"type": "paragraph", "text": "Presence is the ability to dominate a room with your mere existence. It's the feeling others get that \"someone important has arrived\" when you walk in. This quality is a combination of posture, body language, and the energy you project."},

        {"type": "heading", "level": 2, "text": "1.3 Health vs. Aesthetics vs. Performance"},
        {"type": "table", "headers": ["Focus", "Description", "Main Objective"], "rows": [
            ["Functional Aesthetics", "Build a physique that looks strong because it IS strong", "Appearance of power"],
            ["Practical Performance", "Develop useful, real-world strength", "Physical capability"],
            ["Optimized Health", "Maintain an anabolic hormonal environment", "Longevity and vitality"]
        ]},
        {"type": "paragraph", "text": "The ALPHA BODY PROTOCOL operates at the strategic intersection of these three domains. The goal is to build a body that is visually imposing, genuinely strong and capable, and fundamentally resilient and energetic."},

        {"type": "heading", "level": 2, "text": "1.4 The Body as a High-Return Investment"},
        {"type": "paragraph", "text": "Your time, energy, and discipline are finite resources. Few investments compare to building and maintaining a strong body. The return manifests in direct and indirect ways:"},
        {"type": "list", "ordered": False, "items": [
            "Professional Return: Greater respect, increased perception of leadership, more energy and focus.",
            "Social Return: Improvement in how you are perceived, increased attractiveness, presence that commands attention.",
            "Personal Return: Radical self-confidence, transferable mental discipline, resilience to stress."
        ]},

        {"type": "heading", "level": 2, "text": "1.5 The Alpha Mindset: Consistency Over Intensity"},
        {"type": "callout", "style": "tip", "title": "Core Principle", "content": "Consistency trumps intensity. Most men fail not because they don't train hard enough, but because they don't train consistently."},
        {"type": "paragraph", "text": "The true \"Alpha\" is not the man who lifts the most weight in a single day. It is the man who shows up, week after week, month after month, and does the necessary work. Abandon the \"all or nothing\" mentality. Embrace the power of \"something, always.\""},
    ]

    blocks_pt = [
        {"type": "heading", "level": 2, "text": "1.1 A realidade brutal: primeira impressão é física"},
        {"type": "paragraph", "text": "Vamos ser diretos: o mundo julga pela aparência. Antes de você abrir a boca para demonstrar sua inteligência, seu caráter ou seu status, as pessoas ao seu redor já formaram uma opinião baseada na sua presença física."},
        {"type": "paragraph", "text": "Um homem com ombros largos, postura ereta e um aperto de mão firme comunica competência e controle sem dizer uma única palavra. Em contraste, um homem com ombros caídos e postura curvada comunica submissão e passividade."},
        {"type": "callout", "style": "warning", "title": "Cheque de Realidade", "content": "Negar essa realidade não a torna menos verdadeira. A única resposta lógica é usá-la a seu favor."},

        {"type": "heading", "level": 2, "text": "1.2 Respeito, autoridade e presença"},
        {"type": "paragraph", "text": "Respeito não é algo que se pede, é algo que se impõe. Sua presença física é a primeira linha dessa imposição. Autoridade não é apenas sobre o cargo que você ocupa; é sobre a aura que você exala."},
        {"type": "paragraph", "text": "Presença é a capacidade de dominar um ambiente com sua simples existência. É a sensação que os outros têm de que \"alguém importante chegou\" quando você entra em uma sala."},

        {"type": "heading", "level": 2, "text": "1.3 Saúde vs. Estética vs. Performance"},
        {"type": "table", "headers": ["Foco", "Descrição", "Objetivo Principal"], "rows": [
            ["Estética Funcional", "Construir um físico que pareça forte porque ELE É forte", "Aparência de poder"],
            ["Performance Prática", "Desenvolver força útil para o dia a dia", "Capacidade física"],
            ["Saúde Otimizada", "Manter um ambiente hormonal anabólico", "Longevidade e vitalidade"]
        ]},
        {"type": "paragraph", "text": "O ALPHA BODY PROTOCOL opera na interseção estratégica desses três domínios."},

        {"type": "heading", "level": 2, "text": "1.4 O corpo como investimento de alto retorno"},
        {"type": "paragraph", "text": "Seu tempo, energia e disciplina são recursos finitos. O retorno se manifesta de formas diretas e indiretas:"},
        {"type": "list", "ordered": False, "items": [
            "Retorno Profissional: Maior respeito, aumento da percepção de liderança, mais energia e foco.",
            "Retorno Social: Melhora na forma como você é percebido, aumento da atratividade.",
            "Retorno Pessoal: Autoconfiança radical, disciplina mental transferível, resiliência ao estresse."
        ]},

        {"type": "heading", "level": 2, "text": "1.5 Mentalidade Alpha: consistência sobre intensidade"},
        {"type": "callout", "style": "tip", "title": "Princípio Central", "content": "A consistência supera a intensidade. A maioria dos homens falha não porque não treina pesado o suficiente, mas porque não treina de forma consistente."},
        {"type": "paragraph", "text": "O verdadeiro \"Alpha\" não é o homem que levanta mais peso em um único dia. É o homem que aparece, semana após semana, mês após mês, e faz o trabalho necessário."},
    ]

    return {
        "chapter_number": 2,
        "title_en": "The Body as a Social Weapon",
        "title_pt": "Corpo como Arma Social",
        "slug": "body-as-social-weapon",
        "summary_en": "Why physical presence matters, the relationship between body and authority, and the Alpha mindset of consistency.",
        "summary_pt": "Por que a presença física importa, a relação entre corpo e autoridade, e a mentalidade Alpha de consistência.",
        "blocks_en": blocks_en,
        "blocks_pt": blocks_pt,
        "cover_image_url": "images/chapter_2.png",
        "is_free_preview": False,
        "is_published": False,
    }


def create_chapter_2():
    """Create Chapter 2: Minimalist Training."""
    blocks_en = [
        {"type": "heading", "level": 2, "text": "2.1 Principles of Efficient Training"},
        {"type": "paragraph", "text": "If the body is a sculpture, training is the chisel. But contrary to popular belief, you don't need to spend endless hours in the gym. The minimalist approach, when executed correctly, is not only more time-efficient but also superior for building dense, functional strength."},

        {"type": "callout", "style": "info", "title": "Core Principles", "content": "Less is more when done correctly. Focus on compound movements. Linear progression is the engine of growth."},

        {"type": "list", "ordered": False, "items": [
            "Less is more when done correctly: The stimulus for muscle growth comes from intensity and progressive overload, not volume.",
            "Focus on compound movements: Squats, deadlifts, bench presses, and pull-ups are the physique builders par excellence.",
            "Linear progression: The body only adapts if forced to do something it hasn't done before. Add weight to the bar each workout."
        ]},

        {"type": "heading", "level": 2, "text": "2.2 Weekly Structure: 3-4x Per Week"},
        {"type": "paragraph", "text": "Training 3 to 4 days a week provides the perfect balance between stimulus and recovery."},

        {"type": "heading", "level": 3, "text": "Option 1: Full Body - 3x per week"},
        {"type": "table", "headers": ["Day A", "Day B", "Day A"], "rows": [
            ["Squat", "Deadlift", "Squat"],
            ["Bench Press", "Overhead Press", "Bench Press"],
            ["Barbell Row", "Pull-up", "Barbell Row"]
        ]},

        {"type": "heading", "level": 3, "text": "Option 2: Upper/Lower Split - 4x per week"},
        {"type": "table", "headers": ["Day", "Focus", "Main Exercises"], "rows": [
            ["Monday", "Lower - Strength", "Squat, Leg Press, Leg Extension"],
            ["Tuesday", "Upper - Strength", "Bench Press, Barbell Row, Overhead Press"],
            ["Thursday", "Lower - Hypertrophy", "Romanian Deadlift, Lunge, Hamstring Curl"],
            ["Friday", "Upper - Hypertrophy", "Pull-up, Incline Bench Press, Seated Row"]
        ]},

        {"type": "heading", "level": 2, "text": "2.3 The Fundamental Exercises"},
        {"type": "paragraph", "text": "These are the pillars of the protocol. Master them. Progress on them. They are responsible for 90% of your results."},
        {"type": "list", "ordered": True, "items": [
            "Squat: The king of leg exercises. Builds quads, glutes, and hamstrings while strengthening the core.",
            "Deadlift: The ultimate test of overall strength. Recruits virtually every muscle in the body.",
            "Bench Press: The primary builder for chest, shoulders, and triceps.",
            "Overhead Press: The best exercise for building broad, strong shoulders.",
            "Barbell Row: Essential for building a dense, thick back.",
            "Pull-up: The best bodyweight exercise for upper back and biceps."
        ]},

        {"type": "heading", "level": 2, "text": "2.4 Volume, Intensity, and Frequency"},
        {"type": "paragraph", "text": "For fundamental exercises, the 3 to 5 sets of 4 to 6 reps range is ideal. For accessory exercises, 3 sets of 8 to 12 reps is more suitable for hypertrophy."},
        {"type": "callout", "style": "tip", "title": "Progressive Overload", "content": "Each workout, add the smallest possible amount of weight to the bar. If last week you squatted 225 lbs for 5 reps, this week attempt 227.5 lbs."},

        {"type": "heading", "level": 2, "text": "2.5 Active Recovery"},
        {"type": "paragraph", "text": "On rest days, engage in low-intensity activities:"},
        {"type": "list", "ordered": False, "items": [
            "A 30-45 minute walk",
            "Light stretching or yoga",
            "Foam rolling to release tension points"
        ]},
    ]

    blocks_pt = [
        {"type": "heading", "level": 2, "text": "2.1 Princípios do Treino Eficiente"},
        {"type": "paragraph", "text": "Se o corpo é uma escultura, o treino é o cinzel. A abordagem minimalista, quando executada corretamente, não é apenas mais eficiente em termos de tempo, mas também superior para construir força densa e funcional."},

        {"type": "callout", "style": "info", "title": "Princípios Centrais", "content": "Menos é mais quando feito corretamente. Foco em movimentos compostos. Progressão linear é o motor do crescimento."},

        {"type": "list", "ordered": False, "items": [
            "Menos é mais quando feito corretamente: O estímulo para crescimento vem da intensidade e sobrecarga progressiva, não do volume.",
            "Foco em movimentos compostos: Agachamentos, levantamento terra, supinos e barras são os construtores de físico por excelência.",
            "Progressão linear: O corpo só se adapta se for forçado a fazer algo que não fez antes."
        ]},

        {"type": "heading", "level": 2, "text": "2.2 Estrutura Semanal: 3-4x por Semana"},
        {"type": "paragraph", "text": "Treinar de 3 a 4 dias por semana oferece o equilíbrio perfeito entre estímulo e recuperação."},

        {"type": "heading", "level": 3, "text": "Opção 1: Full Body - 3x por semana"},
        {"type": "table", "headers": ["Dia A", "Dia B", "Dia A"], "rows": [
            ["Agachamento", "Levantamento Terra", "Agachamento"],
            ["Supino", "Desenvolvimento", "Supino"],
            ["Remada com Barra", "Barra Fixa", "Remada com Barra"]
        ]},

        {"type": "heading", "level": 3, "text": "Opção 2: Divisão Upper/Lower - 4x por semana"},
        {"type": "table", "headers": ["Dia", "Foco", "Exercícios Principais"], "rows": [
            ["Segunda", "Inferiores - Força", "Agachamento, Leg Press, Extensora"],
            ["Terça", "Superiores - Força", "Supino, Remada, Desenvolvimento"],
            ["Quinta", "Inferiores - Hipertrofia", "Terra Romeno, Afundo, Flexora"],
            ["Sexta", "Superiores - Hipertrofia", "Barra Fixa, Supino Inclinado, Remada Sentada"]
        ]},

        {"type": "heading", "level": 2, "text": "2.3 Os Exercícios Fundamentais"},
        {"type": "paragraph", "text": "Estes são os pilares do protocolo. Domine-os. Progrida neles. Eles são responsáveis por 90% dos seus resultados."},
        {"type": "list", "ordered": True, "items": [
            "Agachamento: O rei dos exercícios para pernas.",
            "Levantamento Terra: O teste definitivo de força total.",
            "Supino: O principal construtor para peitoral, ombros e tríceps.",
            "Desenvolvimento: O melhor exercício para ombros.",
            "Remada com Barra: Essencial para costas densas.",
            "Barra Fixa: O melhor exercício com peso corporal."
        ]},

        {"type": "heading", "level": 2, "text": "2.4 Volume, Intensidade e Frequência"},
        {"type": "paragraph", "text": "Para exercícios fundamentais, a faixa de 3 a 5 séries de 4 a 6 repetições é ideal."},
        {"type": "callout", "style": "tip", "title": "Carga Progressiva", "content": "A cada treino, adicione o mínimo de peso possível à barra. Se na semana passada você agachou 100kg para 5 repetições, nesta semana tente 101kg."},

        {"type": "heading", "level": 2, "text": "2.5 Recuperação Ativa"},
        {"type": "paragraph", "text": "Nos dias de descanso, pratique atividades de baixa intensidade:"},
        {"type": "list", "ordered": False, "items": [
            "Caminhada de 30-45 minutos",
            "Alongamento leve ou yoga",
            "Rolo de espuma para liberar tensão"
        ]},
    ]

    return {
        "chapter_number": 3,
        "title_en": "Minimalist Training",
        "title_pt": "Treino Minimalista",
        "slug": "minimalist-training",
        "summary_en": "The principles of efficient training, weekly structure, fundamental exercises, and progressive overload.",
        "summary_pt": "Os princípios do treino eficiente, estrutura semanal, exercícios fundamentais e sobrecarga progressiva.",
        "blocks_en": blocks_en,
        "blocks_pt": blocks_pt,
        "cover_image_url": "images/chapter_3.png",
        "is_free_preview": False,
        "is_published": False,
    }


def create_chapter_3():
    """Create Chapter 3: Strategic Nutrition."""
    blocks_en = [
        {"type": "heading", "level": 2, "text": "3.1 Nutritional Fundamentals Without Complication"},
        {"type": "paragraph", "text": "If training is what stimulates the muscle to grow, nutrition is what provides the raw materials for that growth to occur. The good news is that the most effective approach is also the simplest."},

        {"type": "heading", "level": 3, "text": "Calorie Balance"},
        {"type": "list", "ordered": False, "items": [
            "Caloric Deficit: Consume fewer calories than you expend = Weight loss",
            "Caloric Maintenance: Consume the same amount = Weight maintenance",
            "Caloric Surplus: Consume more calories than you expend = Weight gain"
        ]},

        {"type": "heading", "level": 3, "text": "Macronutrients"},
        {"type": "table", "headers": ["Macronutrient", "Main Function", "Quality Sources"], "rows": [
            ["Protein", "Building and repairing tissues", "Meats, eggs, fish, dairy, whey"],
            ["Carbohydrates", "Primary energy source", "Rice, potatoes, oats, fruits"],
            ["Fats", "Hormone production, cell health", "Avocado, olive oil, nuts, egg yolks"]
        ]},

        {"type": "heading", "level": 2, "text": "3.2 Protein as a Priority"},
        {"type": "callout", "style": "warning", "title": "Critical Rule", "content": "If there is one macronutrient you must prioritize above all others, it is protein. Protein is the building block of muscle."},
        {"type": "paragraph", "text": "Ideal Amount: 1.6 to 2.2 grams of protein per kilogram of body weight (0.7 to 1.0 grams per pound). An 80kg man should aim for 128-176g of protein per day."},
        {"type": "list", "ordered": False, "items": [
            "Red meat (sirloin, filet)",
            "Chicken and turkey (breast, thigh)",
            "Fish (salmon, tilapia, tuna)",
            "Whole eggs",
            "Dairy (Greek yogurt, cottage cheese)",
            "Whey protein (supplement)"
        ]},

        {"type": "heading", "level": 2, "text": "3.3 Nutrient Density"},
        {"type": "paragraph", "text": "Build 90% of your diet around minimally processed foods. Highly processed foods are calorically dense but nutritionally poor."},

        {"type": "heading", "level": 3, "text": "Essential Shopping List"},
        {"type": "list", "ordered": False, "items": [
            "Eggs",
            "Chicken breast or ground meat",
            "Plain Greek yogurt",
            "Rice and oats",
            "Potatoes",
            "Frozen vegetables",
            "Seasonal fruits",
            "Olive oil and nuts"
        ]},

        {"type": "heading", "level": 2, "text": "3.4 Practical Strategies"},
        {"type": "paragraph", "text": "Find 3-4 meals that you enjoy, that fit your macronutrient goals, and that are easy to prepare. Repeat them."},
        {"type": "callout", "style": "tip", "title": "Meal Prep", "content": "Take 2-3 hours on Sunday to cook most of your proteins and carbohydrates for the week. This eliminates decision-making and makes it impossible not to follow the plan."},

        {"type": "heading", "level": 2, "text": "3.5 Smart Supplementation"},
        {"type": "heading", "level": 3, "text": "What Actually Works:"},
        {"type": "list", "ordered": False, "items": [
            "Whey Protein: Convenient and cost-effective way to hit your daily protein target.",
            "Creatine Monohydrate: The most studied supplement. Take 5 grams per day, every day.",
            "Vitamin D3 and Magnesium: Crucial for testosterone production and overall health."
        ]},
        {"type": "heading", "level": 3, "text": "What is a Waste of Money:"},
        {"type": "paragraph", "text": "Most pre-workouts, BCAAs, \"testosterone boosters,\" and fat-burning pills are mostly ineffective and expensive."},
    ]

    blocks_pt = [
        {"type": "heading", "level": 2, "text": "3.1 Fundamentos Nutricionais Sem Complicação"},
        {"type": "paragraph", "text": "Se o treino é o que estimula o músculo a crescer, a alimentação é o que fornece a matéria-prima para que esse crescimento ocorra."},

        {"type": "heading", "level": 3, "text": "Balanço Calórico"},
        {"type": "list", "ordered": False, "items": [
            "Déficit Calórico: Consumir menos calorias do que gasta = Perda de peso",
            "Manutenção Calórica: Consumir a mesma quantidade = Manutenção do peso",
            "Superávit Calórico: Consumir mais calorias do que gasta = Ganho de peso"
        ]},

        {"type": "heading", "level": 3, "text": "Macronutrientes"},
        {"type": "table", "headers": ["Macronutriente", "Função Principal", "Fontes de Qualidade"], "rows": [
            ["Proteína", "Construção e reparo de tecidos", "Carnes, ovos, peixes, laticínios, whey"],
            ["Carboidratos", "Fonte primária de energia", "Arroz, batatas, aveia, frutas"],
            ["Gorduras", "Produção hormonal, saúde celular", "Abacate, azeite, nozes, gemas"]
        ]},

        {"type": "heading", "level": 2, "text": "3.2 Proteína como Prioridade"},
        {"type": "callout", "style": "warning", "title": "Regra Crítica", "content": "Se há um macronutriente que você deve priorizar acima de todos os outros, é a proteína. A proteína é o bloco de construção do músculo."},
        {"type": "paragraph", "text": "Quantidade Ideal: 1.6 a 2.2 gramas de proteína por quilo de peso corporal. Um homem de 80kg deve visar entre 128g e 176g de proteína por dia."},
        {"type": "list", "ordered": False, "items": [
            "Carne vermelha (patinho, filé)",
            "Frango e peru (peito, coxa)",
            "Peixes (salmão, tilápia, atum)",
            "Ovos inteiros",
            "Laticínios (iogurte grego, cottage)",
            "Whey protein (suplemento)"
        ]},

        {"type": "heading", "level": 2, "text": "3.3 Densidade Nutricional"},
        {"type": "paragraph", "text": "Construa 90% da sua dieta em torno de alimentos minimamente processados."},

        {"type": "heading", "level": 3, "text": "Lista de Compras Essencial"},
        {"type": "list", "ordered": False, "items": [
            "Ovos",
            "Peito de frango ou carne moída",
            "Iogurte grego natural",
            "Arroz e aveia",
            "Batatas",
            "Vegetais congelados",
            "Frutas da estação",
            "Azeite de oliva e nozes"
        ]},

        {"type": "heading", "level": 2, "text": "3.4 Estratégias Práticas"},
        {"type": "paragraph", "text": "Encontre 3-4 refeições que você goste, que se encaixem em suas metas de macronutrientes e que sejam fáceis de preparar. Repita-as."},
        {"type": "callout", "style": "tip", "title": "Preparação de Refeições", "content": "Tire 2-3 horas no domingo para cozinhar a maior parte das suas proteínas e carboidratos para a semana. Isso elimina a tomada de decisão."},

        {"type": "heading", "level": 2, "text": "3.5 Suplementação Inteligente"},
        {"type": "heading", "level": 3, "text": "O que Realmente Funciona:"},
        {"type": "list", "ordered": False, "items": [
            "Whey Protein: Forma conveniente de atingir sua meta diária de proteína.",
            "Creatina Monohidratada: O suplemento mais estudado. Tome 5 gramas por dia.",
            "Vitamina D3 e Magnésio: Cruciais para produção de testosterona."
        ]},
        {"type": "heading", "level": 3, "text": "O que é Desperdício de Dinheiro:"},
        {"type": "paragraph", "text": "A maioria dos pré-treinos, BCAAs, \"testosterone boosters\" e pílulas de queima de gordura são ineficazes e caros."},
    ]

    return {
        "chapter_number": 4,
        "title_en": "Strategic Nutrition",
        "title_pt": "Alimentação Estratégica",
        "slug": "strategic-nutrition",
        "summary_en": "Nutritional fundamentals, protein prioritization, nutrient density, practical strategies, and smart supplementation.",
        "summary_pt": "Fundamentos nutricionais, priorização de proteína, densidade nutricional, estratégias práticas e suplementação inteligente.",
        "blocks_en": blocks_en,
        "blocks_pt": blocks_pt,
        "cover_image_url": "images/chapter_4.png",
        "is_free_preview": False,
        "is_published": False,
    }


def create_chapter_4():
    """Create Chapter 4: Hormones and Optimization."""
    blocks_en = [
        {"type": "paragraph", "text": "Training and nutrition are the visible pillars of building a superior physique. However, beneath the surface, there is a much more powerful layer of control: your endocrine system. Hormones are the chemical messengers that govern virtually every function in your body."},

        {"type": "heading", "level": 2, "text": "4.1 Testosterone: The Alpha Hormone"},
        {"type": "paragraph", "text": "Testosterone is the hormone of masculinity. It drives muscle mass, bone density, libido, ambition levels, and overall sense of well-being. Optimal testosterone levels make everything easier."},

        {"type": "heading", "level": 3, "text": "Factors that Increase Testosterone Naturally:"},
        {"type": "list", "ordered": False, "items": [
            "Heavy Strength Training: Compound movements provoke an acute hormonal response.",
            "Healthy Fats in the Diet: Cholesterol is the precursor to testosterone.",
            "Quality Sleep: Most testosterone production occurs during deep sleep.",
            "Healthy Body Fat Percentage: Stay between 10-15% body fat.",
            "Vitamin D and Zinc: Essential micronutrients for testosterone production."
        ]},

        {"type": "heading", "level": 3, "text": "Factors that Destroy Testosterone:"},
        {"type": "list", "ordered": False, "items": [
            "Chronic stress",
            "Sleep deprivation",
            "Excessive alcohol consumption",
            "Poor diet high in sugar and processed foods",
            "Obesity",
            "Lack of physical activity"
        ]},

        {"type": "heading", "level": 2, "text": "4.2 Cortisol and Stress Management"},
        {"type": "paragraph", "text": "Cortisol is the primary stress hormone. Chronically elevated cortisol levels create a catabolic environment, breaking down muscle tissue and storing fat, especially in the abdominal region."},
        {"type": "callout", "style": "warning", "title": "Key Insight", "content": "Cortisol has an inverse relationship with testosterone: when cortisol is high, testosterone tends to be low."},

        {"type": "heading", "level": 3, "text": "Strategies to Manage Cortisol:"},
        {"type": "list", "ordered": False, "items": [
            "Meditation or Deep Breathing: 10-15 minutes a day.",
            "Avoiding Overtraining: Too much training is a form of stress.",
            "Adequate Sleep: The primary antidote to cortisol.",
            "Hobbies and Leisure: Activities you genuinely enjoy.",
            "Walks in Nature: Proven effect on reducing cortisol."
        ]},

        {"type": "heading", "level": 2, "text": "4.3 Insulin and Metabolic Sensitivity"},
        {"type": "paragraph", "text": "Insulin is a storage hormone. High insulin sensitivity is good (efficient glucose transport). Low sensitivity (insulin resistance) promotes fat storage and blocks fat burning."},

        {"type": "heading", "level": 3, "text": "How to Improve Insulin Sensitivity:"},
        {"type": "list", "ordered": False, "items": [
            "Strength Training: Depletes muscle glycogen, improving sensitivity.",
            "Maintain Low Body Fat: Excess fat causes insulin resistance.",
            "Limit Sugars and Refined Carbohydrates.",
            "Apple Cider Vinegar: Before carb-rich meals.",
            "Cinnamon: Add to meals for a positive effect."
        ]},

        {"type": "heading", "level": 2, "text": "4.4 Growth Hormone and IGF-1"},
        {"type": "paragraph", "text": "Growth Hormone (GH) is crucial for cell repair, muscle growth, and fat burning."},
        {"type": "heading", "level": 3, "text": "How to Increase GH Naturally:"},
        {"type": "list", "ordered": False, "items": [
            "Deep Sleep: Largest release of GH occurs during deep sleep phases.",
            "High-Intensity Training: Sprints and heavy lifting stimulate GH.",
            "Intermittent Fasting: Periods of fasting increase GH levels."
        ]},

        {"type": "heading", "level": 2, "text": "4.5 Habits that Optimize the Hormonal Profile"},
        {"type": "table", "headers": ["Habit", "Specific Action", "Hormonal Impact"], "rows": [
            ["Sun Exposure", "15-20 min direct sun midday", "Increases Vitamin D, raises testosterone"],
            ["Nutrient-Rich Diet", "Meats, eggs, healthy fats, cruciferous vegetables", "Building blocks for hormone production"],
            ["Avoid Endocrine Disruptors", "Minimize plastics, filtered water, natural products", "Reduces xenoestrogen exposure"],
            ["Healthy Competition", "Competitive activities", "Increases dopamine and testosterone"],
            ["Stay Calm Under Pressure", "Diaphragmatic breathing", "Controls cortisol"]
        ]},
    ]

    blocks_pt = [
        {"type": "paragraph", "text": "Treino e nutrição são os pilares visíveis da construção de um físico superior. No entanto, sob a superfície, existe uma camada de controle muito mais poderosa: seu sistema endócrino."},

        {"type": "heading", "level": 2, "text": "4.1 Testosterona: o hormônio alpha"},
        {"type": "paragraph", "text": "A testosterona é o hormônio da masculinidade. É o que impulsiona a massa muscular, densidade óssea, libido, níveis de ambição e sensação geral de bem-estar."},

        {"type": "heading", "level": 3, "text": "Fatores que Aumentam a Testosterona Naturalmente:"},
        {"type": "list", "ordered": False, "items": [
            "Treinamento de Força Pesado: Movimentos compostos provocam resposta hormonal.",
            "Gorduras Saudáveis na Dieta: O colesterol é o precursor da testosterona.",
            "Sono de Qualidade: A maior parte da produção ocorre durante o sono profundo.",
            "Percentual de Gordura Saudável: Mantenha-se entre 10-15%.",
            "Vitamina D e Zinco: Micronutrientes essenciais."
        ]},

        {"type": "heading", "level": 3, "text": "Fatores que Destroem a Testosterona:"},
        {"type": "list", "ordered": False, "items": [
            "Estresse crônico",
            "Privação de sono",
            "Consumo excessivo de álcool",
            "Dieta pobre em nutrientes",
            "Obesidade",
            "Falta de atividade física"
        ]},

        {"type": "heading", "level": 2, "text": "4.2 Cortisol e Gerenciamento de Estresse"},
        {"type": "paragraph", "text": "O cortisol é o principal hormônio do estresse. Níveis cronicamente elevados criam um ambiente catabólico, quebrando tecido muscular e armazenando gordura."},
        {"type": "callout", "style": "warning", "title": "Insight Chave", "content": "O cortisol tem uma relação inversa com a testosterona: quando o cortisol está alto, a testosterona tende a baixar."},

        {"type": "heading", "level": 3, "text": "Estratégias para Gerenciar o Cortisol:"},
        {"type": "list", "ordered": False, "items": [
            "Meditação ou Respiração Profunda: 10-15 minutos por dia.",
            "Evitar o Overtraining: Treinar demais é uma forma de estresse.",
            "Sono Adequado: O principal antídoto do cortisol.",
            "Hobbies e Lazer: Atividades que você genuinamente aprecia.",
            "Caminhadas na Natureza: Efeito comprovado na redução do cortisol."
        ]},

        {"type": "heading", "level": 2, "text": "4.3 Insulina e Sensibilidade Metabólica"},
        {"type": "paragraph", "text": "A insulina é um hormônio de armazenamento. Alta sensibilidade à insulina é boa. Baixa sensibilidade promove armazenamento de gordura."},

        {"type": "heading", "level": 3, "text": "Como Melhorar a Sensibilidade à Insulina:"},
        {"type": "list", "ordered": False, "items": [
            "Treinamento de Força: Esgota o glicogênio muscular.",
            "Manter Baixo Percentual de Gordura.",
            "Limitar Açúcares e Carboidratos Refinados.",
            "Vinagre de Maçã: Antes de refeições ricas em carboidratos.",
            "Canela: Adicionar às refeições."
        ]},

        {"type": "heading", "level": 2, "text": "4.4 Hormônio do Crescimento e IGF-1"},
        {"type": "paragraph", "text": "O Hormônio do Crescimento (GH) é crucial para reparação celular, crescimento muscular e queima de gordura."},
        {"type": "heading", "level": 3, "text": "Como Aumentar o GH Naturalmente:"},
        {"type": "list", "ordered": False, "items": [
            "Sono Profundo: A maior liberação de GH ocorre durante o sono profundo.",
            "Treinamento de Alta Intensidade: Sprints e treino pesado.",
            "Jejum Intermitente: Períodos de jejum aumentam os níveis de GH."
        ]},

        {"type": "heading", "level": 2, "text": "4.5 Hábitos que Otimizam o Perfil Hormonal"},
        {"type": "table", "headers": ["Hábito", "Ação Específica", "Impacto Hormonal"], "rows": [
            ["Exposição Solar", "15-20 min de sol direto ao meio-dia", "Aumenta Vitamina D, eleva testosterona"],
            ["Dieta Rica em Nutrientes", "Carnes, ovos, gorduras saudáveis", "Blocos de construção hormonal"],
            ["Evitar Disruptores Endócrinos", "Minimizar plásticos, água filtrada", "Reduz exposição a xenoestrogênios"],
            ["Competição Saudável", "Atividades competitivas", "Aumenta dopamina e testosterona"],
            ["Calma sob Pressão", "Respiração diafragmática", "Controla o cortisol"]
        ]},
    ]

    return {
        "chapter_number": 5,
        "title_en": "Hormones and Optimization",
        "title_pt": "Hormônios e Otimização",
        "slug": "hormones-optimization",
        "summary_en": "Testosterone optimization, cortisol management, insulin sensitivity, growth hormone, and daily habits for elite hormonal profile.",
        "summary_pt": "Otimização de testosterona, gerenciamento de cortisol, sensibilidade à insulina, hormônio do crescimento e hábitos diários.",
        "blocks_en": blocks_en,
        "blocks_pt": blocks_pt,
        "cover_image_url": "images/chapter_5.png",
        "is_free_preview": False,
        "is_published": False,
    }


def create_chapter_5():
    """Create Chapter 5: Sleep and Recovery."""
    blocks_en = [
        {"type": "paragraph", "text": "You can train with the ferocity of a Spartan and eat with the discipline of a monk, but if your sleep is deficient, you are catastrophically sabotaging your own efforts. Sleep is the most potent and underrated anabolic state at your disposal."},

        {"type": "heading", "level": 2, "text": "5.1 Sleep as the Foundation"},
        {"type": "callout", "style": "warning", "title": "Non-Negotiable", "content": "For most adults, 7 to 9 hours per night is non-negotiable. For men who train intensely, 8-9 hours is ideal."},
        {"type": "paragraph", "text": "Chronically getting less than 7 hours is associated with: lower testosterone levels, increased cortisol, decreased insulin sensitivity, and impaired cognitive function."},

        {"type": "heading", "level": 2, "text": "5.2 Sleep Hygiene"},
        {"type": "heading", "level": 3, "text": "The Ideal Environment (The \"Cave\")"},
        {"type": "list", "ordered": True, "items": [
            "Total Darkness: Use blackout curtains, cover all LEDs, use a sleep mask if necessary.",
            "Absolute Silence: Use earplugs or a white noise generator.",
            "Cool Temperature: Ideal is between 18°C and 20°C (65°F and 68°F)."
        ]},

        {"type": "heading", "level": 3, "text": "The Nightly Routine (Wind-Down Ritual)"},
        {"type": "paragraph", "text": "Create a 30 to 60-minute routine before bed:"},
        {"type": "list", "ordered": False, "items": [
            "Turn Off Screens: At least one hour before bed. Blue light suppresses melatonin.",
            "Read a Physical Book: Under dim, warm light.",
            "Warm Bath: 90 minutes before bed to mimic natural temperature drop.",
            "Light Stretching or Meditation: Releases tension."
        ]},

        {"type": "heading", "level": 3, "text": "What to Avoid Before Bed:"},
        {"type": "list", "ordered": False, "items": [
            "Caffeine: Avoid 8-10 hours before bed.",
            "Alcohol: Destroys sleep quality by suppressing REM sleep.",
            "Heavy Meals: Avoid 2-3 hours before bed.",
            "Intense Exercise: Can raise adrenaline too much."
        ]},

        {"type": "heading", "level": 2, "text": "5.3 Circadian Rhythms"},
        {"type": "list", "ordered": False, "items": [
            "Consistent Schedule: Same bedtime and wake time every day, including weekends.",
            "Morning Sunlight Exposure: 10-15 minutes shortly after waking."
        ]},

        {"type": "heading", "level": 2, "text": "5.4 Muscular and Neural Recovery"},
        {"type": "paragraph", "text": "Recovery has two components:"},
        {"type": "list", "ordered": False, "items": [
            "Muscular Recovery: Repair of muscle fibers. Requires time, protein, and sleep.",
            "Neural Recovery: CNS fatigue from heavy training. Takes longer than muscular recovery."
        ]},

        {"type": "heading", "level": 2, "text": "5.5 Signs of Overtraining"},
        {"type": "table", "headers": ["Category", "Warning Signs"], "rows": [
            ["Performance", "Stagnation or regression in strength; lack of desire to train"],
            ["Physiological", "Elevated resting heart rate; persistent soreness; poor sleep"],
            ["Psychological", "Irritability, mood swings, apathy, difficulty concentrating"],
            ["Immunological", "Getting sick more often"]
        ]},
        {"type": "callout", "style": "tip", "title": "Remember", "content": "You don't get stronger in the gym; you get stronger while you recover from what you did in the gym."},
    ]

    blocks_pt = [
        {"type": "paragraph", "text": "Você pode treinar com a ferocidade de um espartano e comer com a disciplina de um monge, mas se o seu sono for deficiente, você está sabotando seus próprios esforços de maneira catastrófica."},

        {"type": "heading", "level": 2, "text": "5.1 Sono como Fundação"},
        {"type": "callout", "style": "warning", "title": "Não Negociável", "content": "Para a maioria dos adultos, 7 a 9 horas por noite não é negociável. Para homens que treinam intensamente, 8-9 horas é o ideal."},
        {"type": "paragraph", "text": "Menos de 7 horas de forma crônica está associado a: níveis mais baixos de testosterona, aumento do cortisol, diminuição da sensibilidade à insulina."},

        {"type": "heading", "level": 2, "text": "5.2 Higiene do Sono"},
        {"type": "heading", "level": 3, "text": "Ambiente Ideal (A \"Caverna\")"},
        {"type": "list", "ordered": True, "items": [
            "Escuridão Total: Use cortinas blackout, cubra todos os LEDs.",
            "Silêncio Absoluto: Use tampões de ouvido ou gerador de ruído branco.",
            "Temperatura Fria: Ideal entre 18°C e 20°C."
        ]},

        {"type": "heading", "level": 3, "text": "Rotina Noturna (Ritual de Desligamento)"},
        {"type": "paragraph", "text": "Crie uma rotina de 30 a 60 minutos antes de dormir:"},
        {"type": "list", "ordered": False, "items": [
            "Desligue as Telas: Pelo menos uma hora antes de deitar.",
            "Leitura de um Livro Físico: Sob uma luz fraca e quente.",
            "Banho Quente: 90 minutos antes de dormir.",
            "Alongamento Leve ou Meditação: Libera a tensão."
        ]},

        {"type": "heading", "level": 3, "text": "O que Evitar Antes de Dormir:"},
        {"type": "list", "ordered": False, "items": [
            "Cafeína: Evite 8-10 horas antes de dormir.",
            "Álcool: Destrói a qualidade do sono, suprimindo o sono REM.",
            "Refeições Pesadas: Evite 2-3 horas antes de deitar.",
            "Exercício Intenso: Pode elevar demais a adrenalina."
        ]},

        {"type": "heading", "level": 2, "text": "5.3 Ciclos Circadianos"},
        {"type": "list", "ordered": False, "items": [
            "Consistência nos Horários: Mesmo horário de dormir e acordar todos os dias.",
            "Exposição à Luz Solar pela Manhã: 10-15 minutos logo após acordar."
        ]},

        {"type": "heading", "level": 2, "text": "5.4 Recuperação Muscular e Neural"},
        {"type": "paragraph", "text": "A recuperação tem dois componentes:"},
        {"type": "list", "ordered": False, "items": [
            "Recuperação Muscular: Reparação das fibras musculares. Requer tempo, proteína e sono.",
            "Recuperação Neural: Fadiga do SNC do treino pesado. Leva mais tempo que a muscular."
        ]},

        {"type": "heading", "level": 2, "text": "5.5 Sinais de Overtraining"},
        {"type": "table", "headers": ["Categoria", "Sinais de Alerta"], "rows": [
            ["Performance", "Estagnação ou regressão na força; falta de vontade de treinar"],
            ["Fisiológicos", "Frequência cardíaca de repouso elevada; dores persistentes"],
            ["Psicológicos", "Irritabilidade, mudanças de humor, apatia"],
            ["Imunológicos", "Ficar doente com mais frequência"]
        ]},
        {"type": "callout", "style": "tip", "title": "Lembre-se", "content": "Você não fica mais forte na academia; você fica mais forte enquanto se recupera do que fez na academia."},
    ]

    return {
        "chapter_number": 6,
        "title_en": "Sleep and Recovery",
        "title_pt": "Sono e Recuperação",
        "slug": "sleep-recovery",
        "summary_en": "Sleep as the foundation, sleep hygiene, circadian rhythms, muscular and neural recovery, and signs of overtraining.",
        "summary_pt": "Sono como fundação, higiene do sono, ciclos circadianos, recuperação muscular e neural, e sinais de overtraining.",
        "blocks_en": blocks_en,
        "blocks_pt": blocks_pt,
        "cover_image_url": "images/chapter_6.png",
        "is_free_preview": False,
        "is_published": False,
    }


def create_chapter_6():
    """Create Chapter 6: Posture and Presence."""
    blocks_en = [
        {"type": "paragraph", "text": "This chapter focuses on how you \"pilot\" your body in the world. Your posture and physical presence are the external manifestation of all the internal work."},

        {"type": "heading", "level": 2, "text": "6.1 Posture as Body Language"},
        {"type": "paragraph", "text": "Think of posture as the tone of voice of your physical presence."},
        {"type": "list", "ordered": False, "items": [
            "Slumped Posture: Communicates submission, uncertainty, low status. The posture of \"sorry for taking up space.\"",
            "Erect and Open Posture: Communicates confidence, authority, high status. The posture of \"I have the right to be here.\""
        ]},
        {"type": "callout", "style": "info", "title": "The Two-Way Street", "content": "Your posture affects your mental state. Adopting a power pose for just two minutes can increase testosterone and decrease cortisol."},

        {"type": "heading", "level": 2, "text": "6.2 Corrective Exercises"},
        {"type": "table", "headers": ["Exercise", "Objective", "Execution"], "rows": [
            ["Face Pull", "Strengthen upper back and external rotators", "High pulley with rope, 3x15-20 reps"],
            ["Wall Chest Stretch", "Stretch shortened pectoral muscles", "30-45 seconds each side"],
            ["Plank", "Strengthen core muscles", "3 sets to failure"],
            ["Wall Slides", "Improve shoulder mobility", "Keep contact with wall while sliding arms up and down"]
        ]},

        {"type": "heading", "level": 2, "text": "6.3 Walking, Sitting, and Standing with Authority"},
        {"type": "heading", "level": 3, "text": "Walking:"},
        {"type": "paragraph", "text": "Walk with purpose. Head up, looking at the horizon. Swing arms naturally from shoulders. Take deliberate steps."},
        {"type": "heading", "level": 3, "text": "Sitting:"},
        {"type": "paragraph", "text": "Sit on your \"sit bones,\" not your tailbone. Maintain the natural curve of your lower back. Shoulders back and down."},
        {"type": "heading", "level": 3, "text": "Standing:"},
        {"type": "paragraph", "text": "Distribute weight evenly over both feet. Slight contraction in glutes and abdomen. Shoulders back and down, opening your chest."},

        {"type": "heading", "level": 2, "text": "6.4 Diaphragmatic Breathing"},
        {"type": "paragraph", "text": "Diaphragmatic breathing (\"belly breathing\") is the breath of calm and control, unlike short thoracic breathing which is the breath of anxiety."},
        {"type": "heading", "level": 3, "text": "How to Practice:"},
        {"type": "list", "ordered": True, "items": [
            "Lie on your back with knees bent.",
            "Place one hand on chest, one on abdomen.",
            "Inhale slowly through nose, making the abdomen rise.",
            "Exhale slowly through mouth, feeling abdomen lower.",
            "Practice for 5 minutes a day."
        ]},

        {"type": "heading", "level": 2, "text": "6.5 Physical Presence in Daily Life"},
        {"type": "list", "ordered": False, "items": [
            "Eye Contact: Maintain firm, but not aggressive, eye contact.",
            "Speak Slowly and Deliberately: Rushed speech denotes nervousness.",
            "Use Open Gestures: Avoid crossing arms. Show palms.",
            "Firm Handshake: Web to web, complete and confident."
        ]},
    ]

    blocks_pt = [
        {"type": "paragraph", "text": "Este capítulo foca em como você \"pilota\" seu corpo no mundo. Sua postura e presença física são a manifestação externa de todo o trabalho interno."},

        {"type": "heading", "level": 2, "text": "6.1 Postura como Linguagem Corporal"},
        {"type": "paragraph", "text": "Pense na postura como o tom de voz da sua presença física."},
        {"type": "list", "ordered": False, "items": [
            "Postura Curvada: Comunica submissão, incerteza, baixo status. A postura do \"desculpe por ocupar espaço.\"",
            "Postura Ereta e Aberta: Comunica confiança, autoridade, alto status. A postura do \"eu tenho o direito de estar aqui.\""
        ]},
        {"type": "callout", "style": "info", "title": "Via de Mão Dupla", "content": "Sua postura afeta seu estado mental. Adotar uma postura de poder por apenas dois minutos pode aumentar a testosterona e diminuir o cortisol."},

        {"type": "heading", "level": 2, "text": "6.2 Exercícios Corretivos"},
        {"type": "table", "headers": ["Exercício", "Objetivo", "Execução"], "rows": [
            ["Face Pull", "Fortalecer parte superior das costas", "Polia alta com corda, 3x15-20 reps"],
            ["Alongamento de Peitoral", "Alongar músculos peitorais encurtados", "30-45 segundos de cada lado"],
            ["Prancha", "Fortalecer músculos do core", "3 séries até a falha"],
            ["Wall Slides", "Melhorar mobilidade dos ombros", "Manter contato com a parede ao deslizar os braços"]
        ]},

        {"type": "heading", "level": 2, "text": "6.3 Andar, Sentar e Estar de Pé com Autoridade"},
        {"type": "heading", "level": 3, "text": "Andando:"},
        {"type": "paragraph", "text": "Caminhe com propósito. Cabeça erguida, olhando para o horizonte. Balance os braços naturalmente. Passos deliberados."},
        {"type": "heading", "level": 3, "text": "Sentado:"},
        {"type": "paragraph", "text": "Sente-se sobre os \"ossos do assento\", não sobre o cóccix. Mantenha a curva natural da lombar. Ombros para trás e para baixo."},
        {"type": "heading", "level": 3, "text": "De Pé:"},
        {"type": "paragraph", "text": "Distribua o peso uniformemente sobre os dois pés. Leve contração nos glúteos e abdômen. Ombros para trás e para baixo."},

        {"type": "heading", "level": 2, "text": "6.4 Respiração Diafragmática"},
        {"type": "paragraph", "text": "A respiração diafragmática (\"respiração pela barriga\") é a respiração da calma e do controle."},
        {"type": "heading", "level": 3, "text": "Como Praticar:"},
        {"type": "list", "ordered": True, "items": [
            "Deite-se de costas com os joelhos dobrados.",
            "Coloque uma mão sobre o peito e a outra sobre o abdômen.",
            "Inspire lentamente pelo nariz, fazendo o abdômen subir.",
            "Expire lentamente pela boca, sentindo o abdômen baixar.",
            "Pratique por 5 minutos por dia."
        ]},

        {"type": "heading", "level": 2, "text": "6.5 Presença Física no Dia a Dia"},
        {"type": "list", "ordered": False, "items": [
            "Contato Visual: Mantenha contato visual firme, mas não agressivo.",
            "Fale Devagar e Deliberadamente: Fala apressada denota nervosismo.",
            "Use Gestos Abertos: Evite cruzar os braços. Mostre as palmas.",
            "Aperto de Mão Firme: Teia com teia, completo e confiante."
        ]},
    ]

    return {
        "chapter_number": 7,
        "title_en": "Posture and Presence",
        "title_pt": "Postura e Presença",
        "slug": "posture-presence",
        "summary_en": "Posture as body language, corrective exercises, walking/sitting/standing with authority, diaphragmatic breathing, and cultivating physical presence.",
        "summary_pt": "Postura como linguagem corporal, exercícios corretivos, andar/sentar/estar de pé com autoridade, respiração diafragmática e cultivar presença física.",
        "blocks_en": blocks_en,
        "blocks_pt": blocks_pt,
        "cover_image_url": "images/chapter_7.png",
        "is_free_preview": False,
        "is_published": False,
    }


def create_chapter_7():
    """Create Chapter 7: The Complete Protocol."""
    blocks_en = [
        {"type": "paragraph", "text": "Theory without practice is useless. This chapter condenses all the principles into a weekly action plan and a daily checklist."},

        {"type": "heading", "level": 2, "text": "7.1 The Complete Model Week"},
        {"type": "table", "headers": ["Day", "Main Focus", "Key Actions"], "rows": [
            ["Monday", "Workout A (Strength)", "Squat 3x5, Bench Press 3x5, Barbell Row 3x5. Sun exposure. Protein priority."],
            ["Tuesday", "Active Recovery", "30-45 min walk or stretching. Maintain protein goal."],
            ["Wednesday", "Workout B (Strength)", "Deadlift 1x5, Overhead Press 3x5, Pull-ups 3x failure."],
            ["Thursday", "Active Recovery", "Walk, foam rolling, or posture exercises."],
            ["Friday", "Workout A (Volume)", "Same exercises as Workout A with lighter weight, 3x8-10."],
            ["Saturday", "Rest or Active Leisure", "Complete rest or enjoyable activity. One free meal allowed."],
            ["Sunday", "Preparation", "Meal prep for the week. Review and plan next week."]
        ]},

        {"type": "heading", "level": 2, "text": "7.2 Daily Alpha Checklist"},
        {"type": "heading", "level": 3, "text": "Morning:"},
        {"type": "list", "ordered": False, "items": [
            "Wake up on schedule (no snooze)",
            "Hydrate immediately (500ml water)",
            "Sunlight exposure for 10-15 minutes",
            "Meal 1: Rich in protein"
        ]},
        {"type": "heading", "level": 3, "text": "During the Day:"},
        {"type": "list", "ordered": False, "items": [
            "Hit hydration goal (3-4 liters)",
            "Maintain conscious posture",
            "Take breaks to stand up every hour",
            "Meals 2 & 3: Focus on protein and whole foods"
        ]},
        {"type": "heading", "level": 3, "text": "Workout (on training days):"},
        {"type": "list", "ordered": False, "items": [
            "Execute fundamental movements with total focus",
            "Aim to progress (more weight or one more rep)",
            "Post-workout meal: Protein and carbohydrates"
        ]},
        {"type": "heading", "level": 3, "text": "Night:"},
        {"type": "list", "ordered": False, "items": [
            "Last meal 2-3 hours before bed",
            "Turn off all screens 60 minutes before bed",
            "Execute wind-down routine",
            "Ensure room is dark, quiet, and cool",
            "Go to bed at scheduled time"
        ]},

        {"type": "heading", "level": 2, "text": "7.3 Metrics to Track"},
        {"type": "list", "ordered": True, "items": [
            "Training Loads: Log your lifts. Is the weight going up over time?",
            "Body Weight: Weigh weekly, morning, fasted. Trend matters, not daily fluctuations.",
            "Progress Photos: Front, back, side every 4 weeks. Same location, same lighting.",
            "Body Measurements: Chest, waist, arms monthly."
        ]},

        {"type": "heading", "level": 2, "text": "7.4 Adjustments Based on Progress"},
        {"type": "list", "ordered": False, "items": [
            "If strength stalled: Check sleep, eating, consistency. Consider a deload week.",
            "If gaining fat too quickly: Reduce carbs/fats slightly (not protein). More walking.",
            "If not gaining weight/mass: Add more carbs or fats. Increase calories slowly."
        ]},
        {"type": "callout", "style": "tip", "title": "Key Insight", "content": "This protocol is a living system. Listen to your body, track your metrics, and adjust the course as needed."},
    ]

    blocks_pt = [
        {"type": "paragraph", "text": "Teoria sem prática é inútil. Este capítulo condensa todos os princípios em um plano de ação semanal e um checklist diário."},

        {"type": "heading", "level": 2, "text": "7.1 Semana Modelo Completa"},
        {"type": "table", "headers": ["Dia", "Foco Principal", "Ações Chave"], "rows": [
            ["Segunda", "Treino A (Força)", "Agachamento 3x5, Supino 3x5, Remada 3x5. Exposição solar. Prioridade em proteína."],
            ["Terça", "Recuperação Ativa", "Caminhada 30-45 min ou alongamento. Manter meta de proteína."],
            ["Quarta", "Treino B (Força)", "Levantamento Terra 1x5, Desenvolvimento 3x5, Barra Fixa 3x falha."],
            ["Quinta", "Recuperação Ativa", "Caminhada, rolo de espuma, ou exercícios posturais."],
            ["Sexta", "Treino A (Volume)", "Mesmos exercícios do Treino A com carga menor, 3x8-10."],
            ["Sábado", "Descanso ou Lazer", "Descanso completo ou atividade prazerosa. Uma refeição livre permitida."],
            ["Domingo", "Preparação", "Preparação de refeições. Revisar e planejar próxima semana."]
        ]},

        {"type": "heading", "level": 2, "text": "7.2 Checklist Diário Alpha"},
        {"type": "heading", "level": 3, "text": "Manhã:"},
        {"type": "list", "ordered": False, "items": [
            "Acordar no horário (sem soneca)",
            "Hidratar imediatamente (500ml de água)",
            "Exposição à luz solar por 10-15 minutos",
            "Refeição 1: Rica em proteína"
        ]},
        {"type": "heading", "level": 3, "text": "Durante o Dia:"},
        {"type": "list", "ordered": False, "items": [
            "Atingir meta de hidratação (3-4 litros)",
            "Manter postura consciente",
            "Fazer pausas para se levantar a cada hora",
            "Refeições 2 e 3: Foco em proteína e alimentos integrais"
        ]},
        {"type": "heading", "level": 3, "text": "Treino (em dias de treino):"},
        {"type": "list", "ordered": False, "items": [
            "Executar movimentos fundamentais com foco total",
            "Tentar progredir (mais peso ou mais uma rep)",
            "Refeição pós-treino: Proteína e carboidratos"
        ]},
        {"type": "heading", "level": 3, "text": "Noite:"},
        {"type": "list", "ordered": False, "items": [
            "Última refeição 2-3 horas antes de dormir",
            "Desligar todas as telas 60 minutos antes de dormir",
            "Executar rotina de desligamento",
            "Garantir que o quarto esteja escuro, silencioso e frio",
            "Deitar-se no horário programado"
        ]},

        {"type": "heading", "level": 2, "text": "7.3 Métricas para Acompanhar"},
        {"type": "list", "ordered": True, "items": [
            "Cargas no Treino: Anote seus levantamentos. A carga está subindo ao longo do tempo?",
            "Peso Corporal: Pese semanalmente, pela manhã, em jejum. A tendência importa.",
            "Fotos de Progresso: Frente, costas, lado a cada 4 semanas. Mesmo local, mesma iluminação.",
            "Medidas Corporais: Peito, cintura, braços mensalmente."
        ]},

        {"type": "heading", "level": 2, "text": "7.4 Ajustes Conforme Progresso"},
        {"type": "list", "ordered": False, "items": [
            "Se estagnado na força: Verifique sono, alimentação, consistência. Considere semana de deload.",
            "Se ganhando gordura rápido: Reduza carboidratos/gorduras ligeiramente (não proteína). Mais caminhadas.",
            "Se não está ganhando peso/massa: Adicione mais carboidratos ou gorduras. Aumente calorias lentamente."
        ]},
        {"type": "callout", "style": "tip", "title": "Insight Chave", "content": "Este protocolo é um sistema vivo. Ouça seu corpo, acompanhe suas métricas e ajuste o curso conforme necessário."},
    ]

    return {
        "chapter_number": 8,
        "title_en": "The Complete Protocol",
        "title_pt": "Protocolo Completo",
        "slug": "complete-protocol",
        "summary_en": "The complete model week, daily Alpha checklist, metrics to track, and how to adjust based on progress.",
        "summary_pt": "A semana modelo completa, checklist diário Alpha, métricas para acompanhar e como ajustar conforme o progresso.",
        "blocks_en": blocks_en,
        "blocks_pt": blocks_pt,
        "cover_image_url": "images/chapter_8.png",
        "is_free_preview": False,
        "is_published": False,
    }


def create_conclusion():
    """Create Conclusion chapter."""
    blocks_en = [
        {"type": "paragraph", "text": "We have reached the end of this manual, but the beginning of your journey. The ALPHA BODY PROTOCOL is much more than a training and diet program. It is an operating philosophy for life, which uses the body as a starting point to forge discipline, resilience, and unshakable self-confidence."},

        {"type": "heading", "level": 2, "text": "Recap of the Principles"},
        {"type": "list", "ordered": True, "items": [
            "The Body is a Tool: Your physical presence is your first communication with the world.",
            "Minimalist and Intense Training: Growth is stimulated by intensity and progressive overload, not by volume.",
            "Principle-Based Nutrition: Prioritize protein. Build your diet around whole, nutrient-dense foods.",
            "Invisible Optimization: Your hormones, sleep, and posture are the force multipliers.",
            "Consistency Above All: Progress is built through the accumulation of small daily victories."
        ]},

        {"type": "heading", "level": 2, "text": "Next Steps"},
        {"type": "callout", "style": "warning", "title": "Action Required", "content": "Knowledge without action is useless. Your task now is to implement. Start today."},
        {"type": "list", "ordered": True, "items": [
            "Plan your week: Define which days you will train.",
            "Go to the supermarket: Buy the foods from the essential list.",
            "Execute the first workout: Start with weights you can control with good form.",
            "Sleep: Tonight, start your wind-down routine and prioritize 7-9 hours."
        ]},

        {"type": "heading", "level": 2, "text": "Long-Term Mindset"},
        {"type": "paragraph", "text": "There will be no finish line. There will be no moment when you are \"done.\" The pursuit of strength and personal optimization is an infinite game. There will be days when you feel weak. There will be weeks when progress stalls. There will be times when life will try to divert you from the path."},
        {"type": "paragraph", "text": "It is in these moments that the principles of this protocol become your anchor. The goal is not perfection, but persistence. The man who follows this path is not just building a body; he is becoming the type of man who keeps his promises to himself."},
        {"type": "callout", "style": "tip", "title": "Final Truth", "content": "The respectable body you seek is simply the byproduct of becoming a man who refuses to accept mediocrity, in any area of his life."},
        {"type": "paragraph", "text": "Now, stop reading. The work awaits."},
    ]

    blocks_pt = [
        {"type": "paragraph", "text": "Chegamos ao final deste manual, mas ao início da sua jornada. O ALPHA BODY PROTOCOL é muito mais do que um programa de treino e dieta. É uma filosofia operacional para a vida, que usa o corpo como ponto de partida para forjar disciplina, resiliência e autoconfiança inabalável."},

        {"type": "heading", "level": 2, "text": "Recapitulação dos Princípios"},
        {"type": "list", "ordered": True, "items": [
            "O Corpo é uma Ferramenta: Sua presença física é a sua primeira comunicação com o mundo.",
            "Treino Minimalista e Intenso: O crescimento é estimulado pela intensidade e sobrecarga progressiva.",
            "Nutrição Baseada em Princípios: Priorize a proteína. Construa sua dieta em torno de alimentos integrais.",
            "Otimização Invisível: Seus hormônios, sono e postura são os multiplicadores de força.",
            "Consistência Acima de Tudo: O progresso é construído pela acumulação de pequenas vitórias diárias."
        ]},

        {"type": "heading", "level": 2, "text": "Próximos Passos"},
        {"type": "callout", "style": "warning", "title": "Ação Necessária", "content": "O conhecimento sem ação é inútil. Sua tarefa agora é implementar. Comece hoje."},
        {"type": "list", "ordered": True, "items": [
            "Planeje sua semana: Defina quais dias você vai treinar.",
            "Vá ao supermercado: Compre os alimentos da lista essencial.",
            "Execute o primeiro treino: Comece com pesos que você consiga controlar.",
            "Durma: Hoje à noite, comece sua rotina de desligamento e priorize 7-9 horas."
        ]},

        {"type": "heading", "level": 2, "text": "Mentalidade de Longo Prazo"},
        {"type": "paragraph", "text": "Não haverá uma linha de chegada. Não haverá um momento em que você \"terminou\". A busca pela força e pela otimização pessoal é um jogo infinito. Haverá dias em que você se sentirá fraco. Haverá semanas em que o progresso estagnará."},
        {"type": "paragraph", "text": "É nesses momentos que os princípios deste protocolo se tornam sua âncora. O objetivo não é a perfeição, mas a persistência. O homem que segue este caminho não está apenas construindo um corpo; ele está se tornando o tipo de homem que cumpre suas promessas a si mesmo."},
        {"type": "callout", "style": "tip", "title": "Verdade Final", "content": "O corpo respeitável que você busca é simplesmente o subproduto de se tornar um homem que se recusa a aceitar a mediocridade, em qualquer área da sua vida."},
        {"type": "paragraph", "text": "Agora, pare de ler. O trabalho espera."},
    ]

    return {
        "chapter_number": 9,
        "title_en": "Conclusion",
        "title_pt": "Conclusão",
        "slug": "conclusion",
        "summary_en": "Recap of principles, next steps to implement, and the long-term mindset for lasting transformation.",
        "summary_pt": "Recapitulação dos princípios, próximos passos para implementar e a mentalidade de longo prazo.",
        "blocks_en": blocks_en,
        "blocks_pt": blocks_pt,
        "cover_image_url": "images/chapter_9.png",
        "is_free_preview": False,
        "is_published": False,
    }


def create_resources():
    """Create Additional Resources chapter."""
    blocks_en = [
        {"type": "paragraph", "text": "This section provides practical tools to help you implement the protocol effectively."},

        {"type": "heading", "level": 2, "text": "Table 1: Protein and Calorie Calculator"},
        {"type": "heading", "level": 3, "text": "Daily Protein Requirements"},
        {"type": "table", "headers": ["Body Weight (kg/lbs)", "Minimum Protein (g)", "Optimal Protein (g)"], "rows": [
            ["60 kg / 132 lbs", "96 g", "132 g"],
            ["70 kg / 154 lbs", "112 g", "154 g"],
            ["80 kg / 176 lbs", "128 g", "176 g"],
            ["90 kg / 198 lbs", "144 g", "198 g"],
            ["100 kg / 220 lbs", "160 g", "220 g"]
        ]},

        {"type": "heading", "level": 3, "text": "Calorie Calculation"},
        {"type": "paragraph", "text": "Maintenance Calories: Body weight (lbs) x 15 or Body weight (kg) x 33"},
        {"type": "list", "ordered": False, "items": [
            "For Fat Loss (Deficit): Subtract 300-500 calories from maintenance.",
            "For Mass Gain (Surplus): Add 200-300 calories to maintenance."
        ]},

        {"type": "heading", "level": 2, "text": "Table 2: Food Sources and Macronutrients"},
        {"type": "heading", "level": 3, "text": "Proteins (per 100g)"},
        {"type": "table", "headers": ["Food", "Protein (g)", "Carbs (g)", "Fat (g)"], "rows": [
            ["Chicken Breast", "25g", "0g", "2g"],
            ["Ground Sirloin", "22g", "0g", "8g"],
            ["Tilapia", "20g", "0g", "2g"],
            ["Egg (1 large)", "6g", "<1g", "5g"],
            ["Whey Protein (1 scoop)", "24g", "3g", "1g"]
        ]},

        {"type": "heading", "level": 3, "text": "Carbohydrates (per 100g)"},
        {"type": "table", "headers": ["Food", "Protein (g)", "Carbs (g)", "Fat (g)"], "rows": [
            ["White Rice (cooked)", "3g", "28g", "0g"],
            ["Sweet Potato", "2g", "20g", "0g"],
            ["Rolled Oats", "14g", "60g", "7g"]
        ]},

        {"type": "heading", "level": 3, "text": "Fats (per 100g/serving)"},
        {"type": "table", "headers": ["Food", "Protein (g)", "Carbs (g)", "Fat (g)"], "rows": [
            ["Avocado", "2g", "9g", "15g"],
            ["Almonds (handful)", "6g", "6g", "14g"],
            ["Olive Oil (1 tbsp)", "0g", "0g", "14g"]
        ]},

        {"type": "heading", "level": 2, "text": "Table 3: Fundamental Exercises Description"},
        {"type": "table", "headers": ["Exercise", "Primary Muscles", "Brief Description"], "rows": [
            ["Barbell Squat", "Quadriceps, Glutes, Adductors", "Bar on back, squat until hips below knees, drive floor to stand"],
            ["Deadlift", "Back, Glutes, Hamstrings", "Bar from floor, extend hips and knees simultaneously"],
            ["Bench Press", "Pectorals, Shoulders, Triceps", "Lower bar to mid-chest, push up explosively"],
            ["Overhead Press", "Shoulders, Triceps", "Bar at collarbone, press overhead with tight core"],
            ["Barbell Row", "Back (Lats, Rhomboids)", "Torso bent forward, pull bar to lower abdomen"],
            ["Pull-up", "Back (Lats), Biceps", "Pull body up until chin over bar, lower controlled"]
        ]},
    ]

    blocks_pt = [
        {"type": "paragraph", "text": "Esta seção fornece ferramentas práticas para ajudá-lo a implementar o protocolo de forma eficaz."},

        {"type": "heading", "level": 2, "text": "Tabela 1: Calculadora de Proteína e Calorias"},
        {"type": "heading", "level": 3, "text": "Necessidades Diárias de Proteína"},
        {"type": "table", "headers": ["Peso Corporal (kg)", "Proteína Mínima (g)", "Proteína Ótima (g)"], "rows": [
            ["60 kg", "96 g", "132 g"],
            ["70 kg", "112 g", "154 g"],
            ["80 kg", "128 g", "176 g"],
            ["90 kg", "144 g", "198 g"],
            ["100 kg", "160 g", "220 g"]
        ]},

        {"type": "heading", "level": 3, "text": "Cálculo de Calorias"},
        {"type": "paragraph", "text": "Calorias de Manutenção: Peso corporal (kg) x 33"},
        {"type": "list", "ordered": False, "items": [
            "Para Perda de Gordura (Déficit): Subtraia 300-500 calorias da manutenção.",
            "Para Ganho de Massa (Superávit): Adicione 200-300 calorias à manutenção."
        ]},

        {"type": "heading", "level": 2, "text": "Tabela 2: Fontes de Alimentos e Macronutrientes"},
        {"type": "heading", "level": 3, "text": "Proteínas (por 100g)"},
        {"type": "table", "headers": ["Alimento", "Proteína (g)", "Carboidratos (g)", "Gordura (g)"], "rows": [
            ["Peito de Frango", "25g", "0g", "2g"],
            ["Patinho Moído", "22g", "0g", "8g"],
            ["Tilápia", "20g", "0g", "2g"],
            ["Ovo (1 unidade)", "6g", "<1g", "5g"],
            ["Whey Protein (1 scoop)", "24g", "3g", "1g"]
        ]},

        {"type": "heading", "level": 3, "text": "Carboidratos (por 100g)"},
        {"type": "table", "headers": ["Alimento", "Proteína (g)", "Carboidratos (g)", "Gordura (g)"], "rows": [
            ["Arroz Branco (cozido)", "3g", "28g", "0g"],
            ["Batata Doce", "2g", "20g", "0g"],
            ["Aveia em Flocos", "14g", "60g", "7g"]
        ]},

        {"type": "heading", "level": 3, "text": "Gorduras (por 100g/porção)"},
        {"type": "table", "headers": ["Alimento", "Proteína (g)", "Carboidratos (g)", "Gordura (g)"], "rows": [
            ["Abacate", "2g", "9g", "15g"],
            ["Amêndoas (punhado)", "6g", "6g", "14g"],
            ["Azeite de Oliva (1 colher)", "0g", "0g", "14g"]
        ]},

        {"type": "heading", "level": 2, "text": "Tabela 3: Descrição dos Exercícios Fundamentais"},
        {"type": "table", "headers": ["Exercício", "Músculos Primários", "Descrição Breve"], "rows": [
            ["Agachamento com Barra", "Quadríceps, Glúteos, Adutores", "Barra nas costas, agachar até quadris abaixo dos joelhos"],
            ["Levantamento Terra", "Costas, Glúteos, Isquiotibiais", "Barra do chão, estender quadris e joelhos simultaneamente"],
            ["Supino Reto", "Peitoral, Ombros, Tríceps", "Descer barra até o meio do peito, empurrar explosivamente"],
            ["Desenvolvimento Militar", "Ombros, Tríceps", "Barra na clavícula, empurrar acima da cabeça com core firme"],
            ["Remada com Barra", "Costas (Latíssimo, Romboides)", "Tronco inclinado, puxar barra para abdômen inferior"],
            ["Barra Fixa", "Costas (Latíssimo), Bíceps", "Puxar corpo até queixo passar da barra, descer controlado"]
        ]},
    ]

    return {
        "chapter_number": 10,
        "title_en": "Additional Resources",
        "title_pt": "Recursos Adicionais",
        "slug": "additional-resources",
        "summary_en": "Protein and calorie calculator, food sources and macronutrients, and fundamental exercises descriptions.",
        "summary_pt": "Calculadora de proteína e calorias, fontes de alimentos e macronutrientes, e descrições dos exercícios fundamentais.",
        "blocks_en": blocks_en,
        "blocks_pt": blocks_pt,
        "cover_image_url": "images/chapter_10.png",
        "is_free_preview": False,
        "is_published": False,
    }


def escape_sql(value):
    """Escape a string for SQL insertion."""
    if value is None:
        return "NULL"
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"


def generate_sql(ebook: dict, chapters: list, total_time: int) -> str:
    """Generate SQL seed file content."""
    lines = [
        "-- E-book Seed File",
        f"-- Generated: {datetime.now().isoformat()}",
        f"-- Title: {ebook['title_en']}",
        "",
        "-- Insert ebook",
        "INSERT INTO ebooks (",
        "  id, title_en, title_pt, slug, description_en, description_pt,",
        "  cover_image_url, price_usd, price_brl, estimated_read_time_minutes, status",
        ") VALUES (",
        f"  '{ebook['id']}',",
        f"  {escape_sql(ebook['title_en'])},",
        f"  {escape_sql(ebook['title_pt'])},",
        f"  {escape_sql(ebook['slug'])},",
        f"  {escape_sql(ebook['description_en'])},",
        f"  {escape_sql(ebook['description_pt'])},",
        f"  {escape_sql(ebook['cover_image_url'])},",
        f"  {ebook['price_usd']},",
        f"  {ebook['price_brl']},",
        f"  {total_time},",
        f"  {escape_sql(ebook['status'])}",
        ");",
        "",
        "-- Insert chapters",
    ]

    for ch in chapters:
        ch_id = str(uuid.uuid4())
        lines.extend([
            f"INSERT INTO chapters (",
            "  id, ebook_id, chapter_number, title_en, title_pt, slug,",
            "  cover_image_url, content_en, content_pt, summary_en, summary_pt,",
            "  estimated_read_time_minutes, is_free_preview, is_published",
            ") VALUES (",
            f"  '{ch_id}',",
            f"  '{ch['ebook_id']}',",
            f"  {ch['chapter_number']},",
            f"  {escape_sql(ch['title_en'])},",
            f"  {escape_sql(ch['title_pt'])},",
            f"  {escape_sql(ch['slug'])},",
            f"  {escape_sql(ch['cover_image_url'])},",
            f"  {escape_sql(ch['content_en'])},",
            f"  {escape_sql(ch['content_pt'])},",
            f"  {escape_sql(ch['summary_en'])},",
            f"  {escape_sql(ch['summary_pt'])},",
            f"  {ch['estimated_read_time_minutes']},",
            f"  {str(ch['is_free_preview']).lower()},",
            f"  {str(ch['is_published']).lower()}",
            ");",
            "",
        ])

    return "\n".join(lines)


def generate_image_prompts(chapters: list) -> str:
    """Generate image prompts for cover and chapters."""
    prompts = [
        "=" * 60,
        "IMAGE PROMPTS FOR ALPHA BODY PROTOCOL",
        "=" * 60,
        "",
        "COVER IMAGE:",
        "Dark cinematic book cover for 'ALPHA BODY PROTOCOL'. Abstract representation of masculine power and strength. Silhouette of a powerful male figure with geometric shapes suggesting muscle and structure. Color palette: deep blacks, dark reds, orange accents. Epic scale, dramatic lighting. No text, no faces. Movie poster quality.",
        "",
    ]

    for ch in chapters:
        prompts.extend([
            f"CHAPTER {ch['chapter_number']}: {ch['title_en']}",
            f"Dark cinematic image representing '{ch['title_en']}'. Abstract, symbolic imagery. {ch['summary_en'][:100]}... Color palette: deep blacks, reds, orange electric accents. Dramatic lighting, cinematic shadows. No text, no faces, no human figures. Epic scale.",
            "",
        ])

    prompts.extend([
        "=" * 60,
        "INSTRUCTIONS:",
        "Use these prompts with any image generation service.",
        "Recommended: Midjourney, DALL-E 3, or Stable Diffusion XL",
        "=" * 60,
    ])

    return "\n".join(prompts)


if __name__ == "__main__":
    generate_seed()

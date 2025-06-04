#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

def subject_pass(lang):
    """
    External function to translate
    """

    if lang == "ca":
        subject = "Dr.Scratch: ¿Ha oblidat la seva contrasenya?"
    elif lang == "es":
        subject = "Dr.Scratch: ¿Olvidaste tu contraseña?"
    elif lang == "en":
        subject = "Dr.Scratch: Did you forget your password?"
    elif lang == "gl":
        subject = "Dr.Scratch: Esqueciches o teu contrasinal?"
    elif lang == "pt":
        subject = "Dr.Scratch: Esqueceu sua senha?"
    elif lang == "el":
        subject = "Dr.Scratch: Ξεχάσατε τον κωδικό σας;"
    elif lang == "eu":
        subject = "Dr.Scratch: Did you forget your password?"
    return subject


def subject_welcome_organization(lang):
    """
    External function to translate
    """

    if lang == "ca":
        subject = "Benvingut a Dr.Scratch per a les organitzacions"
    elif lang == "es":
        subject = "Bienvenido a Dr.Scratch para organizaciones"
    elif lang == "en":
        subject = "Welcome to Dr.Scratch for organizations"
    elif lang == "gl":
        subject = "Benvido ao Dr.Scratch para organizacións"
    elif lang == "pt":
        subject = "Bem-vindo ao Dr.Scratch para organizações"
    elif lang == "el":
        subject = "Καλώς ήρθατε στο Dr.Scratch για τους οργανισμούς"
    elif lang == "eu":
        subject = "Welcome to Dr.Scratch for organizations"
    return subject


def subject_welcome_coder(lang):
    """
    External function to translate
    """

    if lang == "ca":
        subject = "Benvingut a Dr.Scratch!"
    elif lang == "es":
        subject = "¡Bienvenido a Dr.Scratch!"
    elif lang == "en":
        subject = "Welcome to Dr.Scratch!"
    elif lang == "gl":
        subject = "Benvido ao Dr.Scratch!"
    elif lang == "pt":
        subject = "Bem-vindo ao Dr.Scratch!"
    elif lang == "el":
        subject = "Καλώς ήρθατε στο Dr.Scratch!"
    elif lang == "en":
        subject = "Welcome to Dr.Scratch!"
    return subject


def skills_translation(request) -> dict:
    """
    Create a dict with the skills name translated
    """
    if request.LANGUAGE_CODE == "en":
        dic = {u'Logic': 'Logic',
               u'Parallelism':'Parallelism',
               u'Data representation':'Data representation',
               u'Synchronization':'Synchronization',
               u'User interactivity':'User interactivity',
               u'Flow control':'Flow control',
               u'Abstraction':'Abstraction',
               u'Math operators':'Math operators',
               u'Motion operators': 'Motion operators'}
    elif request.LANGUAGE_CODE == "es":
        #page = unicodedata.normalize('NFKD',page).encode('ascii', 'ignore')
        dic = {'Pensamiento lógico':'Logic',
               'Paralelismo':'Parallelism',
               'Representación de la información':'Data representation',
               'Sincronización':'Synchronization',
               'Interactividad con el usuario':'User',
               'Control de flujo':'Flow control',
               'Abstracción':'Abstraction',
               'Operadores matemáticos':'Math operators',
               'Operadores de movimiento': 'Motion operators'}
    elif request.LANGUAGE_CODE == "ca":
        #page = unicodedata.normalize('NFKD', page).encode('ascii', 'ignore')
        dic = {u'Lògica':'Logic',
               u'Paral·lelisme':'Parallelism',
               u'Representació de dades':'Data representation',
               u'Sincronització':'Synchronization',
               u"Interactivitat de l'usuari":'User interactivity',
               u'Controls de flux':'Flow control',
               u'Abstracció':'Abstraction',
               u'Operadors matemàtics':'Math operators',
               u'Operadors de moviment': 'Motion operators'}
    elif request.LANGUAGE_CODE == "gl":
        #page = unicodedata.normalize('NFKD',page).encode('ascii', 'ignore')
        dic = {'Lóxica':'Logic',
               'Paralelismo':'Parallelism',
               'Representación dos datos':'Data representation',
               'Sincronización':'Synchronization',
               'Interactividade do susario':'User interactivity',
               'Control de fluxo':'Flow control',
               'Abstracción':'Abstraction',
               'Operadores matemáticos':'Math operators',
               'Operadores de movemento': 'Motion operators'}
    elif request.LANGUAGE_CODE == "pt":
        #page = unicodedata.normalize('NFKD',page).encode('ascii', 'ignore')
        dic = {'Lógica':'Logic',
               'Paralelismo':'Parallelism',
               'Representação de dados':'Data representation',
               'Sincronização':'Synchronization',
               'Interatividade com o usuário':'User interactivity',
               'Controle de fluxo':'Flow control',
               'Abstração':'Abstraction',
               'Operadores matemáticos':'Math operators',
               'Operadores de movimento': 'Motion operators'}
    elif request.LANGUAGE_CODE == "el":
        dic = {u'Λογική':'Logic',
           u'Παραλληλισμός':'Parallelism',
           u'Αναπαράσταση δεδομένων':'Data representation',
           u'Συγχρονισμός':'Synchronization',
           u'Αλληλεπίδραση χρήστη':'User interactivity',
           u'Έλεγχος ροής':'Flow control',
           u'Αφαίρεση':'Abstraction',
           u'Μαθηματικοί χειριστές':'Math operators',
           u'Χειριστές κίνησης': 'Motion operators'}
    elif request.LANGUAGE_CODE == "eu":
        #page = unicodedata.normalize('NFKD',page).encode('ascii', 'ignore')
        dic = {u'Logika':'Logic',
           u'Paralelismoa':'Parallelism',
           u'Datu adierazlea':'Data representation',
           u'Sinkronizatzea':'Synchronization',
           u'Erabiltzailearen elkarreragiletasuna':'User interactivity',
           u'Kontrol fluxua':'Flow control',
           u'Abstrakzioa':'Abstraction',
           u'Eragile matematikoak':'Math operators',
           u'Mugimendu-eragileak': 'Motion operators'}
    elif request.LANGUAGE_CODE == "it":
        #page = unicodedata.normalize('NFKD',page).encode('ascii','ignore')
        dic = {u'Logica':'Logic',
           u'Parallelismo':'Parallelism',
           u'Rappresentazione dei dati':'Data representation',
           u'Sincronizzazione':'Synchronization',
           u'Interattività utente':'User interactivity',
           u'Controllo di flusso':'Flow control',
           u'Astrazione':'Abstraction',
           u'Operatori matematici':'Math operators',
           u'Operatori del movimento': 'Motion operators'}
    elif request.LANGUAGE_CODE == "ru":
        dic = {u'Логика': 'Logic',
               u'Параллельность действий': 'Parallelism',
               u'Представление данных': 'Data representation',
               u'cинхронизация': 'Synchronization',
               u'Интерактивность': 'User interactivity',
               u'Управление потоком': 'Flow control',
               u'Абстракция': 'Abstraction',
               u'Математические операторы':'Math operators',
               u'Операторы движения': 'Motion operators'}
    elif request.LANGUAGE_CODE == "tr":
        dic = {
            u'Logic': 'Mantık',
            u'Parallelism': 'Paralellik',
            u'Data representation': 'Veri temsili',
            u'Synchronization': 'Senkranizasyon',
            u'User interactivity': 'Kullanıcı etkileşimi',
            u'Flow control': 'Akış kontrolü',
            u'Abstraction': 'Soyutlama',
            u'Math operators': 'Matematiksel operatörler',
            u'Motion operators': 'Hareket operatörleri'}
    else:
        dic = {u'Logica':'Logic',
               u'Paralelismo':'Parallelism',
               u'Representacao':'Data representation',
               u'Sincronizacao':'Synchronization',
               u'Interatividade':'User interactivity',
               u'Controle':'Flow control',
               u'Abstracao':'Abstraction',
               u'Operadores matemáticos':'Math operators',
               u'Operadores de movimento': 'Motion operators'}
    return dic


def translate(request, d, filename, vanilla=False):
    """
    Translate the output of Hairball
    """

    if request.LANGUAGE_CODE == "es":
        d_translate_es = {'Abstracción': [d['Abstraction'], 'Abstraction'], 'Paralelismo': [d['Parallelization'], 'Parallelization'],
                          'Pensamiento lógico': [d['Logic'], 'Logic'], 'Sincronización': [d['Synchronization'], 'Synchronization'],
                          'Control de flujo': [d['FlowControl'], 'FlowControl'], 'Interactividad con el usuario': [d['UserInteractivity'], 'UserInteractivity'],
                          'Representación de la información': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: # Check that not is Vanilla Mode
            d_translate_es.update({'Operadores matemáticos': [d['MathOperators'], 'MathOperators'], 'Operadores de movimiento': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "es"
        filename.save()
        return d_translate_es
    elif request.LANGUAGE_CODE == "en":
        d_translate_en = {'Abstraction': [d['Abstraction'], 'Abstraction'], 'Parallelism': [d['Parallelization'], 'Parallelization'], 'Logic': [d['Logic'], 'Logic'],
                          'Synchronization': [d['Synchronization'], 'Synchronization'], 'Flow control': [d['FlowControl'], 'FlowControl'],
                          'User interactivity': [d['UserInteractivity'], 'UserInteractivity'], 'Data representation': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_en.update({'Math operators': [d['MathOperators'], 'MathOperators'], 'Motion operators': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "en"
        filename.save()
        return d_translate_en
    elif request.LANGUAGE_CODE == "ca":
        d_translate_ca = {'Abstracció': [d['Abstraction'], 'Abstraction'], 'Paral·lelisme': [d['Parallelization'], 'Parallelization'], 'Lògica': [d['Logic'], 'Logic'],
                          'Sincronització': [d['Synchronization'], 'Synchronization'], 'Controls de flux': [d['FlowControl'], 'FlowControl'],
                          "Interactivitat de l'usuari": [d['UserInteractivity'], 'UserInteractivity'],
                          'Representació de dades': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_ca.update({'Operadors matemàtics': [d['MathOperators'], 'MathOperators'], 'Operadors de moviment':  [d['MotionOperators'], 'MotionOperators']})
        filename.language = "ca"
        filename.save()
        return d_translate_ca
    elif request.LANGUAGE_CODE == "gl":
        d_translate_gl = {'Abstracción': [d['Abstraction'], 'Abstraction'], 'Paralelismo': [d['Parallelization'], 'Parallelization'], 'Lóxica': [d['Logic'], 'Logic'],
                          'Sincronización': [d['Synchronization'], 'Synchronization'], 'Control de fluxo': [d['FlowControl'], 'FlowControl'],
                          "Interactividade do susario": [d['UserInteractivity'], 'UserInteractivity'],
                          'Representación dos datos': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_gl.update({'Operadores matemáticos': [d['MathOperators'], 'MathOperators'], 'Operadores de movemento': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "gl"
        filename.save()
        return d_translate_gl

    elif request.LANGUAGE_CODE == "pt":
        d_translate_pt = {'Abstração': [d['Abstraction'], 'Abstraction'], 'Paralelismo': [d['Parallelization'], 'Parallelization'], 'Lógica': [d['Logic'], 'Logic'],
                          'Sincronização': [d['Synchronization'], 'Synchronization'], 'Controle de fluxo': [d['FlowControl'], 'FlowControl'],
                          "Interatividade com o usuário": [d['UserInteractivity'], 'UserInteractivity'],
                          'Representação de dados': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_pt.update({'Operadores matemáticos': [d['MathOperators'], 'MathOperators'], 'Operadores de movimento': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "pt"
        filename.save()
        return d_translate_pt
    
    elif request.LANGUAGE_CODE == "el":
        d_translate_el = {'Αφαίρεση': [d['Abstraction'], 'Abstraction'], 'Παραλληλισμός': [d['Parallelization'], 'Parallelization'], 'Λογική': [d['Logic'], 'Logic'],
                          'Συγχρονισμός': [d['Synchronization'], 'Synchronization'], 'Έλεγχος ροής': [d['FlowControl'], 'FlowControl'],
                          'Αλληλεπίδραση χρήστη': [d['UserInteractivity'], 'UserInteractivity'],
                          'Αναπαράσταση δεδομένων': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_el.update({'Μαθηματικοί χειριστές': [d['MathOperators'], 'MathOperators'], 'Χειριστές κίνησης': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "el"
        filename.save()
        return d_translate_el

    elif request.LANGUAGE_CODE == "eu":           
        d_translate_eu = {'Abstrakzioa': [d['Abstraction'], 'Abstraction'], 'Paralelismoa': [d['Parallelization'], 'Parallelization'], 'Logika': [d['Logic'], 'Logic'],
                          'Sinkronizatzea': [d['Synchronization'], 'Synchronization'], 'Kontrol fluxua': [d['FlowControl'], 'FlowControl'],
                          'Erabiltzailearen elkarreragiletasuna': [d['UserInteractivity'], 'UserInteractivity'],
                          'Datu adierazlea': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_eu.update({'Eragile matematikoak': [d['MathOperators'], 'MathOperators'], 'Mugimendu-eragileak': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "eu"
        filename.save()
        return d_translate_eu

    elif request.LANGUAGE_CODE == "it":           
        d_translate_it = {'Astrazione': [d['Abstraction'], 'Abstraction'], 'Parallelismo': [d['Parallelization'], 'Parallelization'], 'Logica': [d['Logic'], 'Logic'],
                          'Sincronizzazione': [d['Synchronization'], 'Synchronization'], 'Controllo di flusso': [d['FlowControl'], 'FlowControl'],
                          'Interattività utente': [d['UserInteractivity'], 'UserInteractivity'],
                          'Rappresentazione dei dati': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_it.update({'Operatori matematici':  [d['MathOperators'], 'MathOperators'], 'Operatori del movimento': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "it"
        filename.save()
        return d_translate_it

    elif request.LANGUAGE_CODE == "ru":
        d_translate_ru = {'Абстракция': [d['Abstraction'], 'Abstraction'], 'Параллельность действий': [d['Parallelization'], 'Parallelization'],
                          'Логика': [d['Logic'], 'Logic'], 'cинхронизация': [d['Synchronization'], 'Synchronization'],
                          'Управление потоком': [d['FlowControl'], 'FlowControl'], 'Интерактивность': [d['UserInteractivity'], 'UserInteractivity'],
                          'Представление данных': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_ru.update({'Математические операторы': [d['MathOperators'], 'MathOperators'], 'Операторы движения': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "ru"
        filename.save()
        return d_translate_ru

    elif request.LANGUAGE_CODE == "tr":
        d_translate_tr = {
            'Soyutlama': [d['Abstraction'], 'Abstraction'], 'Paralellik': [d['Parallelization'], 'Parallelization'],
            'Mantık': [d['Logic'], 'Logic'], 'Senkranizasyon': [d['Synchronization'], 'Synchronization'],
            'Akış kontrolü': [d['FlowControl'], 'FlowControl'], 'Kullanıcı etkileşimi': [d['UserInteractivity'], 'UserInteractivity'],
            'Veri temsili': [d['DataRepresentation'], 'DataRepresentation']
        }
        if not vanilla: 
            d_translate_tr.update({'Matematiksel operatörler': [d['MathOperators'], 'MathOperators'], 'Hareket operatörleri': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "tr"
        filename.save()
        return d_translate_tr

    else:
        d_translate_en = {'Abstraction': [d['Abstraction'], 'Abstraction'], 'Parallelism': [d['Parallelization'], 'Parallelization'], 'Logic': [d['Logic'], 'Logic'],
                          'Synchronization': [d['Synchronization'], 'Synchronization'], 'Flow control': [d['FlowControl'], 'FlowControl'],
                          'User interactivity': [d['UserInteractivity'], 'UserInteractivity'], 'Data representation': [d['DataRepresentation'], 'DataRepresentation']}
        if not vanilla: 
            d_translate_en.update({'Math Operators': [d['MathOperators'], 'MathOperators'], 'Motion Operators': [d['MotionOperators'], 'MotionOperators']})
        filename.language = "any"
        filename.save()
        return d_translate_en
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
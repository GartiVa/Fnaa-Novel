import random
import os

nochi = {
    1: (100, 16, ("Бонито",)),
    2: (90, 18, ("Бонито", "Чикита")),
    3: (85, 24, ("Бонито", "Чикита", "Фоксито")),
    4: (75, 28, ("Бонито", "Чикита", "Фоксито", "Фредерито")),
}

komnati = {
    1: "Сцена",
    2: "Обеденный зал",
    3: "Кухня",
    4: "Коридор",
    5: "Офис",
}

monstri = {
    "Фредерито": {"slabost": "код", "info": "Хитрый. Боится кода щитка."},
    "Бонито": {"slabost": "дверь", "info": "Быстрый. Дверь его останавливает."},
    "Чикита": {"slabost": "еда", "info": "Голодная. Отвлеки её едой."},
    "Фоксито": {"slabost": "фонарик", "info": "Самый быстрый. Не замирает, боится света."},
}

kod_ot_shitka = {"код": ""}
chasti_koda = {}

inventar = []
jurnal = []

smotrel_kameri = set()
zakritie_dveri = set()
sobrannie_batareyki = set()
naydennie_chasti = set()

SHIRINA = 66


def ochistit_ekran():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def centr(text, shirina=SHIRINA):
    return text.center(shirina)


def liniya(simvol="=", shirina=SHIRINA):
    return simvol * shirina


def zagolovok(nazvanie, simvol="="):
    print(liniya(simvol))
    print(centr(nazvanie))
    print(liniya(simvol))


def otbit_bonito(pozicii, dver_zakrita):
    if pozicii["Бонито"] == 5 and dver_zakrita:
        pozicii["Бонито"] = 0
        return True, "Бонито ударился в дверь и убежал!"
    return False, ""


def otbit_chikitu(pozicii, inventar):
    if pozicii["Чикита"] in (4, 5) and "еда" in inventar:
        pozicii["Чикита"] = 0
        return True, "Чикита отвлечена едой!"
    return False, ""


def otbit_foksito(pozicii, inventar):
    if pozicii["Фоксито"] == 5 and "фонарик" in inventar:
        pozicii["Фоксито"] = 0
        return True, "Фоксито отпугнут фонариком!"
    return False, ""


def otbit_frederito(pozicii):
    if pozicii["Фредерито"] >= 5:
        pozicii["Фредерито"] = 0
        return True, "Фредерито вырублен кодом щитка!"
    return False, ""


def pokazat_pomosh():
    ochistit_ekran()
    zagolovok("ПАМЯТКА ОХРАННИКУ")
    print()
    print("  КАК ИГРАТЬ:")
    print("    - Ты ночной охранник. Аниматроники ползут к тебе по камерам.")
    print("    - Доживи до 6:00 (конец ходов) - ночь пройдена.")
    print()
    print("  ЭНЕРГИЯ:")
    print("    - Базовый расход (свет, приборы): -1 каждый ход")
    print("    - Пропустить ход: -2")
    print("    - Смотреть камеры: -3")
    print("    - Закрыть дверь: -3")
    print("    - Фонарик: -3 (тратится всегда)")
    print("    - Закрытая дверь пассивно съедает еще -3")
    print()
    print("  ВАЖНО:")
    print("    - Фоксито и Фредерито НЕ ВИДНЫ на камерах (кроме 1-й).")
    print("    - Фредерито телепортируется и смеется 'Ха-ха!'. На 3-й раз он в офисе!")
    print("    - Части кода спрятаны на камерах.")
    print()
    input("  Нажми Enter, чтобы вернуться...")


def pokazat_spravochnik():
    ochistit_ekran()
    zagolovok("СПРАВОЧНИК: ПРОТИВ КОГО ЧТО РАБОТАЕТ")
    print()
    print("  БОНИТО")
    print("    Слабость: ДВЕРЬ")
    print("    Совет: закрой дверь, когда он на камере 5 (Офис).")
    print()
    print("  ЧИКИТА")
    print("    Слабость: ЕДА (использовать на камерах 4 и 5)")
    print()
    print("  ФОКСИТО")
    print("    Слабость: ФОНАРИК")
    print("    Совет: увидеть его можно только на 1 камере и использовать фонарик на 5 камере.")
    print("           и использовать фонарик на 5 камере, на камерах можно найти батарейки.")
    print()
    print("  ФРЕДЕРИТО")
    print("    Слабость: КОД ЩИТКА")
    print("    Совет: собирай части кода и слушай его смех.")
    print()
    input("  Нажми Enter, чтобы вернуться...")


def pokazat_avtorov():
    ochistit_ekran()
    zagolovok("АВТОРЫ")
    print()
    print(centr("Кудреватых Сергей"))
    print(centr("Коржаков Константин"))
    print(centr("Группа: П-3-25"))
    print()
    input("  Нажми Enter, чтобы вернуться...")


def narisovat_ekran(energiya, hod, vsego_hodov, noch, deistviya, inventar, zakritie_dveri, soobsheniya):
    ochistit_ekran()
    zagolovok(f"FIVE NIGHTS AT ANIMATRONICS   |   НОЧЬ {noch}")

    sostoyanie = [
        f"Ход: {hod}/{vsego_hodov}",
        f"Энергия: {energiya}%",
        f"Инвентарь: {', '.join(inventar) if inventar else 'пусто'}",
        f"Дверь: {'ЗАКРЫТА' if zakritie_dveri else 'открыта'}",
    ]

    shirina_levo = 32
    shirina_pravo = SHIRINA - shirina_levo - 4

    print(f"  {'ДЕЙСТВИЯ':<{shirina_levo}}  {'СОСТОЯНИЕ':<{shirina_pravo}}")
    print(liniya("-"))

    maks_strok = max(len(deistviya), len(sostoyanie))
    for i in range(maks_strok):
        levo = deistviya[i] if i < len(deistviya) else ""
        pravo = sostoyanie[i] if i < len(sostoyanie) else ""
        print(f"  {levo:<{shirina_levo}}  {pravo}")

    print(liniya("-"))
    if soobsheniya:
        for msg in soobsheniya:
            print(centr(msg))
    else:
        print(centr("Выбери действие цифрой и нажми Enter"))
    print(liniya("-"))


def vibrat_iz_menyu(nazvanie, varianty):
    while True:
        ochistit_ekran()
        zagolovok(nazvanie)
        print()
        for i, opt in enumerate(varianty, 1):
            print(centr(f"{i}. {opt}"))
        print(centr("0. Назад"))
        print(liniya("-"))
        vibor = input("  Твой выбор: ").strip()
        if vibor == "0":
            return None
        if vibor.isdigit() and 1 <= int(vibor) <= len(varianty):
            return int(vibor) - 1
        print(centr("Неверный выбор, попробуй ещё раз."))
        input("  Enter...")


def posmotret_kameru(kamera, pozicii, aktivnie, noch, energiya, smotrel_kameri, kameri_s_batareykami, kameri_s_kodom):
    smotrel_kameri.add(kamera)
    tekushaya_kamera = kamera
    
    kto = []
    for imya in aktivnie:
        if pozicii[imya] == kamera:
            if imya in ("Фоксито", "Фредерито"):
                if kamera == 1:
                    kto.append(imya)
            else:
                kto.append(imya)

    if kto:
        msg = f"Камера {kamera} ({komnati[kamera]}). Видно: {', '.join(kto)}"
    else:
        msg = f"Камера {kamera} ({komnati[kamera]}). Пусто."
        
    if noch >= 3 and kamera in kameri_s_batareykami and kamera not in sobrannie_batareyki:
        msg += " (Тут лежит батарейка!)"
    if noch == 4 and kamera in kameri_s_kodom and kamera not in naydennie_chasti:
        nomer, znachenie = chasti_koda[kamera]
        msg += f" (На стене {nomer} часть кода: {znachenie})"
    
    return energiya, msg, smotrel_kameri, tekushaya_kamera


def zakrit_dver(energiya, zakritie_dveri):
    if zakritie_dveri:
        return energiya, "Дверь уже закрыта.", zakritie_dveri
    zakritie_dveri.add(5)
    energiya -= 3
    return energiya, "Дверь закрыта.", zakritie_dveri


def otkrit_dver(zakritie_dveri):
    if not zakritie_dveri:
        return "Дверь уже открыта.", zakritie_dveri
    zakritie_dveri.discard(5)
    return "Дверь открыта.", zakritie_dveri


def ispolzovat_fonarik(pozicii, aktivnie, inventar):
    otbil, msg = otbit_foksito(pozicii, inventar)
    if otbil:
        return True, msg
    return False, "Фонарик никого не напугал."


def ispolzovat_edu(pozicii, aktivnie, inventar):
    otbil, msg = otbit_chikitu(pozicii, inventar)
    if otbil:
        return True, msg
    return False, "Еда никого не отвлекла."


def vvesti_kod(pozicii, soobsheniya):
    vveden = input("  Введи код щитка (Enter - отмена): ").strip()
    if not vveden:
        soobsheniya.append("Ты не ввёл код. Ход не потрачен.")
        return False
    
    if vveden == kod_ot_shitka["код"]:
        otbil, msg = otbit_frederito(pozicii)
        soobsheniya.append(msg)
        if not otbil:
            soobsheniya.append("Код верный, но Фредерито еще не в офисе.")
        return True
    else:
        soobsheniya.append("Неверный код!")
        return True


def dvigat_monstrov(pozicii, aktivnie, zakritie_dveri, soobsheniya, haha_count):
    for imya in aktivnie:
        tekushaya = pozicii[imya]
        
        if imya == "Бонито":
            otbil, msg = otbit_bonito(pozicii, 5 in zakritie_dveri)
            if otbil:
                soobsheniya.append(msg)
                continue

        if imya == "Фредерито":
            if haha_count == 0:
                shans = 0.5
            elif haha_count == 1:
                shans = 0.3
            else:
                shans = 0.3 
                
            if random.random() < shans:
                kto_na_5 = [n for n in aktivnie if pozicii[n] == 5 and n != imya]
                if haha_count >= 2 and kto_na_5:
                    continue 
                
                haha_count += 1
                soobsheniya.append("Ха-ха!")
                
                if haha_count == 1:
                    pozicii[imya] = 2
                elif haha_count == 2:
                    pozicii[imya] = 4
                elif haha_count >= 3:
                    pozicii[imya] = 5
            continue

        if imya != "Фоксито" and random.random() < 0.25:
            continue
        
        sleduyushaya = tekushaya + 1 if tekushaya < 6 else tekushaya

        if sleduyushaya == 5:
            kto_na_5 = [n for n in aktivnie if pozicii[n] == 5 and n != imya]
            if kto_na_5:
                continue

        pozicii[imya] = sleduyushaya

        if pozicii[imya] == 5 and imya == "Бонито":
            soobsheniya.append("Бонито подошёл к камере 5!")

        if imya == "Бонито":
            otbil, msg = otbit_bonito(pozicii, 5 in zakritie_dveri)
            if otbil:
                soobsheniya.append(msg)

    return haha_count


def proverit_porazhenie(pozicii, aktivnie):
    for imya in aktivnie:
        if pozicii[imya] >= 6:
            return imya
    return None


def igrat_noch(noch, inventar, jurnal, zakritie_dveri, smotrel_kameri):
    energiya, vsego_hodov, aktivnie = nochi[noch]
    pozicii = {imya: 0 for imya in aktivnie}

    zakritie_dveri.clear()
    smotrel_kameri.clear()
    sobrannie_batareyki.clear()
    naydennie_chasti.clear()
    
    tekushaya_kamera = 1
    haha_count = 0

    if noch == 1:
        inventar = ["фонарик"]
    elif noch >= 2:
        inventar = ["фонарик", "еда"]

    kameri_s_batareykami = []
    if noch == 3:
        kameri_s_batareykami = [random.choice([1, 2, 3, 4])]
    elif noch == 4:
        kameri_s_batareykami = random.sample([1, 2, 3, 4], 2)

    kameri_s_kodom = []
    if noch == 4:
        kameri_s_kodom = random.sample([1, 2, 3, 4], 2)
        p1 = str(random.randint(10, 99))
        p2 = str(random.randint(10, 99))
        kod_ot_shitka["код"] = p1 + p2
        chasti_koda.clear()
        chasti_koda[kameri_s_kodom[0]] = ("первая", p1)
        chasti_koda[kameri_s_kodom[1]] = ("вторая", p2)

    hod = 1
    soobsheniya = []
    while hod <= vsego_hodov:
        menyu = [
            "Смотреть камеры",
            "Закрыть дверь",
            "Открыть дверь",
        ]
        if noch >= 2:
            menyu.append("Использовать еду")
        if noch >= 3:
            menyu.append("Использовать фонарик")
        if len(sobrannie_batareyki) < len(kameri_s_batareykami):
            menyu.append("Взять батарейку")
        if noch == 4:
            menyu.append("Ввести код щитка")
        menyu.append("Пропустить ход")
        menyu.append("Помощь")

        narisovat_ekran(energiya, hod, vsego_hodov, noch, [f"{i+1}. {m}" for i, m in enumerate(menyu)], inventar, zakritie_dveri, soobsheniya)
        
        vibor = input("  > ").strip()
        
        soobsheniya = []
        
        if not vibor.isdigit() or not (1 <= int(vibor) <= len(menyu)):
            soobsheniya.append("Неверный выбор.")
            continue

        deistvie = menyu[int(vibor) - 1]

        if deistvie == "Смотреть камеры":
            kamery = [f"{v}" for k, v in komnati.items()]
            vibrano = vibrat_iz_menyu("КАМЕРЫ", kamery)
            if vibrano is None:
                continue
            
            haha_count = dvigat_monstrov(pozicii, aktivnie, zakritie_dveri, soobsheniya, haha_count)
            
            energiya, msg, smotrel_kameri, tekushaya_kamera = posmotret_kameru(vibrano + 1, pozicii, aktivnie, noch, energiya, smotrel_kameri, kameri_s_batareykami, kameri_s_kodom)
            soobsheniya.append(msg)
            energiya -= 3

        elif deistvie == "Закрыть дверь":
            if zakritie_dveri:
                soobsheniya.append("Дверь уже закрыта.")
                continue
            energiya, msg, zakritie_dveri = zakrit_dver(energiya, zakritie_dveri)
            soobsheniya.append(msg)
            
            haha_count = dvigat_monstrov(pozicii, aktivnie, zakritie_dveri, soobsheniya, haha_count)
            
            energiya, msg, smotrel_kameri, tekushaya_kamera = posmotret_kameru(tekushaya_kamera, pozicii, aktivnie, noch, energiya, smotrel_kameri, kameri_s_batareykami, kameri_s_kodom)
            soobsheniya.append(msg)
            energiya -= 3

        elif deistvie == "Открыть дверь":
            if not zakritie_dveri:
                soobsheniya.append("Дверь уже открыта.")
                continue
            msg, zakritie_dveri = otkrit_dver(zakritie_dveri)
            soobsheniya.append(msg)
            
            haha_count = dvigat_monstrov(pozicii, aktivnie, zakritie_dveri, soobsheniya, haha_count)
            
            energiya, msg, smotrel_kameri, tekushaya_kamera = posmotret_kameru(tekushaya_kamera, pozicii, aktivnie, noch, energiya, smotrel_kameri, kameri_s_batareykami, kameri_s_kodom)
            soobsheniya.append(msg)

        elif deistvie == "Использовать фонарик":
            otbil, msg = ispolzovat_fonarik(pozicii, aktivnie, inventar)
            soobsheniya.append(msg)
            
            haha_count = dvigat_monstrov(pozicii, aktivnie, zakritie_dveri, soobsheniya, haha_count)
            
            energiya, msg, smotrel_kameri, tekushaya_kamera = posmotret_kameru(tekushaya_kamera, pozicii, aktivnie, noch, energiya, smotrel_kameri, kameri_s_batareykami, kameri_s_kodom)
            soobsheniya.append(msg)
            energiya -= 3

        elif deistvie == "Использовать еду":
            otbil, msg = ispolzovat_edu(pozicii, aktivnie, inventar)
            soobsheniya.append(msg)
            if not otbil:
                soobsheniya.append("Ход не потрачен.")
                continue
            
            haha_count = dvigat_monstrov(pozicii, aktivnie, zakritie_dveri, soobsheniya, haha_count)
            
            energiya, msg, smotrel_kameri, tekushaya_kamera = posmotret_kameru(tekushaya_kamera, pozicii, aktivnie, noch, energiya, smotrel_kameri, kameri_s_batareykami, kameri_s_kodom)
            soobsheniya.append(msg)

        elif deistvie == "Взять батарейку":
            if tekushaya_kamera in kameri_s_batareykami and tekushaya_kamera not in sobrannie_batareyki:
                sobrannie_batareyki.add(tekushaya_kamera)
                energiya += 15
                soobsheniya.append("Ты подобрал батарейку (+15 энергии).")
                energiya, msg, smotrel_kameri, tekushaya_kamera = posmotret_kameru(tekushaya_kamera, pozicii, aktivnie, noch, energiya, smotrel_kameri, kameri_s_batareykami, kameri_s_kodom)
                soobsheniya.append(msg)
            else:
                soobsheniya.append("Здесь нет батарейки.")
                continue

        elif deistvie == "Ввести код щитка":
            vvel = vvesti_kod(pozicii, soobsheniya)
            if not vvel:
                continue
            haha_count = dvigat_monstrov(pozicii, aktivnie, zakritie_dveri, soobsheniya, haha_count)

        elif deistvie == "Пропустить ход":
            soobsheniya.append("Ты решил ничего не делать.")
            haha_count = dvigat_monstrov(pozicii, aktivnie, zakritie_dveri, soobsheniya, haha_count)
            energiya -= 2

        elif deistvie == "Помощь":
            pokazat_pomosh()
            continue

        if 5 in zakritie_dveri:
            energiya -= 3

        energiya -= 1

        hod += 1

        mertv = proverit_porazhenie(pozicii, aktivnie)
        if mertv:
            ochistit_ekran()
            zagolovok(f"{mertv} добрался до офиса. Ты проиграл!")
            input("  Нажми Enter...")
            return False, inventar, jurnal, zakritie_dveri, smotrel_kameri

        if energiya <= 0:
            ochistit_ekran()
            zagolovok("Энергия кончилась. Ты проиграл!")
            input("  Нажми Enter...")
            return False, inventar, jurnal, zakritie_dveri, smotrel_kameri

    ochistit_ekran()
    zagolovok(f"6:00 - НОЧЬ {noch} ПРОЙДЕНА")
    input("  Нажми Enter...")
    return True, inventar, jurnal, zakritie_dveri, smotrel_kameri


def igrat(inventar, jurnal, zakritie_dveri, smotrel_kameri):
    ochistit_ekran()
    zagolovok("FIVE NIGHTS AT ANIMATRONICS")
    print(centr("Продержись 4 ночи. Удачи, охранник."))
    print()
    imya = input("  Как тебя зовут, ночной охранник? ").strip() or "Охранник"
    ochistit_ekran()
    zagolovok(f"Добро пожаловать, {imya}")
    input("  Нажми Enter, чтобы начать ночь 1...")

    for noch in range(1, 5):
        uspeh, inventar, jurnal, zakritie_dveri, smotrel_kameri = igrat_noch(noch, inventar, jurnal, zakritie_dveri, smotrel_kameri)
        if not uspeh:
            print(centr("ИГРА ОКОНЧЕНА. Попробуй снова."))
            input("  Нажми Enter...")
            return inventar, jurnal, zakritie_dveri, smotrel_kameri
        
        input(f"  Нажми Enter, чтобы перейти к ночи {noch + 1}...")

    ochistit_ekran()
    zagolovok("ТЫ ПРОДЕРЖАЛСЯ ВСЕ 4 НОЧИ!")
    print(centr("Ты - легенда пиццерии 67."))
    print()
    input("  Нажми Enter...")
    
    return inventar, jurnal, zakritie_dveri, smotrel_kameri


def main():
    inventar = []
    jurnal = []
    zakritie_dveri = set()
    smotrel_kameri = set()

    while True:
        ochistit_ekran()
        zagolovok("FIVE NIGHTS AT ANIMATRONICS")
        print(centr("Текстовая новелла на Python"))
        print()
        print(centr("1. Играть"))
        print(centr("2. Справочник"))
        print(centr("3. Помощь"))
        print(centr("4. Авторы"))
        print(centr("5. Выход"))
        print()
        print(liniya("-"))
        vibor = input("  Твой выбор: ").strip()

        if vibor == "1":
            inventar, jurnal, zakritie_dveri, smotrel_kameri = igrat(inventar, jurnal, zakritie_dveri, smotrel_kameri)
        elif vibor == "2":
            pokazat_spravochnik()
        elif vibor == "3":
            pokazat_pomosh()
        elif vibor == "4":
            pokazat_avtorov()
        elif vibor == "5":
            ochistit_ekran()
            print()
            print(centr("До следующей смены, охранник..."))
            print()
            return
        else:
            print(centr("Неверный выбор."))
            input("  Нажми Enter...")

if __name__ == "__main__":
    main()

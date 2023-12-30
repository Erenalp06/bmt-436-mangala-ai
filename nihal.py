def evaluation_function():
    node_keys = {"k1": "4", "k2": "4", "k3": "4", "k4": "4", "k5": "4", "k6": "4", "k7": "0",
                 "k8": "4", "k9": "4", "k10": "4", "k11": "4", "k12": "4", "k13": "4", "k14": "0"}
    counter = 0
    kontrol_sarti = 0
    #karşısınddaki oyuncunun kuyusundaki taslar çift yaparsan hem tasları al hemde son koydugun tası al
    hedef_konum = int(node_keys["k1"]) + (int(node_keys["k1"])-1)
    if hedef_konum > 7 :
        hedef_kuyu_no = "k"+str(hedef_konum)
        kuyu_tas = int(node_keys[hedef_kuyu_no])
        if kuyu_tas % 2 == 1:
            funcb_deger = kuyu_tas + 1

    #kendi tarafında boş bir kuyuya tek bir taş atarsam karşı(rakibin kuyusudaki) taşları ve boş kuyuya attığın taşı al.

    if node_keys[hedef_kuyu_no] == "0" and hedef_konum < 7:
        karsı_kuyu_konum = "k"+ str( 14 - hedef_konum)
        funcc_deger = int (node_keys[karsı_kuyu_konum]) + 1

    if funcb_deger > funcc_deger:
        donus_degeri = funcb_deger
    elif funcc_deger > funcb_deger:
        donus_degeri = funcc_deger
    elif funcc_deger == funcb_deger:
        donus_degeri = funcc_deger

    #oyun bitti mi kontrol et(iki tarafın da kuyuları boş mu buna bakar)

    for key in node_keys.keys():
        if key != "k7" or key != ("k14"):
            if node_keys[key] == "0":
                counter += 1

    if counter == 12:
        print("oyun bitti")
        donus_degeri = 0
        kontrol_sarti = 1

    return donus_degeri





    #while döngüsü ile sürekli çağırulabilir.Kontorl sartı == 0 iken.
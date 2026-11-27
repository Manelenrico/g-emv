"""[P8] Prompt 147 (taller): RG69r+voz, la reserva (cuerpo_rg69.RG69, prompt 146) más la voz de ir a casa (cuerpo_vc1.VC1, prompt 143), EXACTAMENTE como
estaban: aquí no hay código de ninguna de las dos, solo se juntan. RG68r, las clases congeladas, cuerpo_valle.py y el mundo no se tocan.
LA FONTANERÍA (lo único nuevo, sin ningún número): una clase hija de las dos, RG69V(VC1, RG69). Python las encadena en ese orden (VC1, RG69,
cuerpo_valle.Criatura): los métodos de la voz (actua, filas, la segunda foto) llaman con super() a los de siempre, y las cuentas de la reserva (vivir_bien,
falta_comida) son las de RG69. Así la voz mira con el cuerpo de RG69r: en la segunda foto (la hermana imaginada en casa) y en la foto de quien la oye, comer
también usa la reserva. Los interruptores: a_casa (de VC1) y reserva_v69 (de RG69). Con a_casa apagado, actua es la de siempre: es RG69r."""
import cuerpo_vc1 as VC
import cuerpo_rg69 as RZ


class RG69V(VC.VC1, RZ.RG69):
    pass

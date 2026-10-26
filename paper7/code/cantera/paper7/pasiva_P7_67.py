"""[P7-67, decision 1 de la mesa] LA POLITICA PASIVA que ocupa los asientos sobrantes: se conecta, no reparte puntos (el juego pone los de por defecto) y a cada observacion
responde «nada» (no se mueve, no coge, no ataca). No tiene cuerpo G-EMV ni diario: solo tres lineas a la salida (player_config, final y fin) para saber que estuvo.
  python3 pasiva_P7_67.py   (la url la pone la plataforma: COWORLD_PLAYER_WS_URL o COGAMES_ENGINE_WS_URL)"""
import asyncio, json, os, time

NADA = {"type": "action", "do": "none"}


def log(rec): print(json.dumps(rec, separators=(",", ":")), flush=True)


async def run(url):
    import websockets
    t0 = time.time(); n = 0
    try:
        async with websockets.connect(url, ping_timeout=None) as ws:
            async for raw in ws:
                try: msg = json.loads(raw)
                except Exception: continue
                t = msg.get("type")
                if t == "observation": await ws.send(json.dumps(NADA)); n += 1
                elif t == "player_config": log({"k": "P7_67_pasiva", "slot": msg.get("slot"), "team": msg.get("team")})
                elif t == "final": log({"k": "final", "observaciones": n, "final": {k: v for k, v in msg.items() if k != "type"}})
    except websockets.exceptions.ConnectionClosed as ex: log({"k": "cierre_sin_aviso", "error": repr(ex)[:120]})      # [humo local] el juego cierra sin trama de cierre al acabar
    log({"k": "fin", "observaciones": n, "segundos": round(time.time() - t0, 1)})


if __name__ == "__main__":
    asyncio.run(run(os.environ.get("COWORLD_PLAYER_WS_URL") or os.environ["COGAMES_ENGINE_WS_URL"]))

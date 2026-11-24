#!/usr/bin/env python3
"""Estado del proyecto de marca: puntos de validación, versiones, pendientes y registro de decisiones.

Un solo archivo (expediente/project-state.json) guarda el estado; `md` genera a partir de él
project/decisiones.md, la versión legible que va dentro del Design System.

Uso:
  python3 estado.py init <estado.json> --empresa "Acme" --objetivo "..." [--profundidad completa|expres]
        [--naming undecided|retain|create|change] [--nombre-existente "Acme"] [--entregable "..."]... [--aprueba usuario]
  python3 estado.py preparar <estado.json> H02 --salida "expediente/plataforma-v1.md" [--salida ...]
  python3 estado.py aprobar  <estado.json> H02 --ref "mensaje del usuario, 2026-11-23" [--actor usuario]
  python3 estado.py cambios  <estado.json> H02 --ref "..." --nota "qué pidió cambiar"
  python3 estado.py nueva-version <estado.json> H02 --motivo "..."
  python3 estado.py alcance <estado.json> [--naming ...] [--nombre-existente ...] [--entregable ...] [--anadir-entregable ...]
  python3 estado.py pendiente <estado.json> "Registrar la marca en la OEPM"   |   --hecho 2
  python3 estado.py mantenimiento <estado.json> --responsable "..." --cambios "..."
  python3 estado.py validar <estado.json> [--punto H02]
  python3 estado.py md <estado.json> --salida project/decisiones.md

Códigos de salida de `validar`: 0 estado coherente (y, con --punto, ese punto aceptado);
1 archivo o estado inválido; 2 estado coherente pero el punto pedido aún no está aceptado.

El script comprueba estructura y dependencias. No comprueba que una aprobación sea auténtica ni la calidad
del trabajo: registra como aprobado solo lo que la persona aprobó de verdad, con la referencia a su mensaje.
Basado en el validador del sistema crear-branding (Codex), portado a Python y ampliado con la profundidad Exprés.
"""
import argparse
import datetime as dt
import json
import sys

DEPENDENCIAS = {
    "H00": [], "H01": ["H00"], "H02": ["H01"], "H03_N": ["H02"], "H03_V": ["H02"],
    "H03_S": ["H03_N", "H03_V"], "H04": ["H03_S"],
}
PUNTOS = list(DEPENDENCIAS)
QUE = {
    "H00": "Alcance", "H01": "Diagnóstico", "H02": "Plataforma", "H03_N": "Nombre",
    "H03_V": "Ruta visual", "H03_S": "Sistema aplicado", "H04": "Entrega",
}
ESTADOS = {"draft", "blocked", "ready_for_review", "approved", "changes_requested", "needs_review", "not_applicable"}
ETIQUETA = {
    "draft": "Borrador", "blocked": "Bloqueado", "ready_for_review": "Listo para revisar", "approved": "Aprobado",
    "changes_requested": "Cambios pedidos", "needs_review": "Pendiente de revisión", "not_applicable": "No aplica",
}
NAMING = {"undecided", "retain", "create", "change"}


def hoy():
    return dt.date.today().isoformat()


def texto(v):
    return isinstance(v, str) and v.strip() != ""


def entero(v):
    return isinstance(v, int) and not isinstance(v, bool) and v > 0


def no_aplica_permitido(estado, punto):
    pr = estado["project"]
    if pr.get("depth") == "expres" and punto in ("H01", "H03_N"):
        return True
    return punto == "H03_N" and pr["scope"].get("naming") == "retain" and texto(pr["scope"].get("existing_name"))


def padres(estado, punto):
    if no_aplica_permitido(estado, punto) and punto in ("H01", "H03_N"):
        return ["H00"]
    return DEPENDENCIAS[punto]


def validar(estado, pedido=None):
    errores = []
    locales = {p: [] for p in PUNTOS}
    aceptado = {}

    def fallo(p, msg):
        e = f"{p}: {msg}"
        errores.append(e)
        locales.setdefault(p, []).append(e)

    def parar(msg):
        return {"valid": False, "errors": [msg], "accepted": [], "pending": PUNTOS, "can_start": []}

    if not isinstance(estado, dict) or estado.get("schema_version") not in (1, 2):
        return parar("schema_version debe ser 1 o 2.")
    pr = estado.get("project")
    if not isinstance(pr, dict) or not isinstance(pr.get("scope"), dict):
        return parar("Falta project.scope.")
    cps = estado.get("checkpoints")
    if not isinstance(cps, dict):
        return parar("Falta checkpoints.")
    if pedido and pedido not in PUNTOS:
        return parar("Punto de validación desconocido.")
    alc = pr["scope"]
    if alc.get("naming") not in NAMING:
        errores.append("project.scope.naming inválido.")
    if not isinstance(alc.get("deliverables"), list) or not all(texto(x) for x in alc.get("deliverables", [])):
        errores.append("project.scope.deliverables debe ser una lista de textos.")
    if pr.get("depth", "completa") not in ("completa", "expres"):
        errores.append("project.depth debe ser completa o expres.")
    for extra in [k for k in cps if k not in PUNTOS]:
        errores.append(f"Punto desconocido: {extra}.")

    for p in PUNTOS:
        g = cps.get(p)
        if not isinstance(g, dict):
            fallo(p, "falta el registro.")
            continue
        if not entero(g.get("version")):
            fallo(p, "version debe ser un entero positivo.")
        if g.get("status") not in ESTADOS:
            fallo(p, "status inválido.")
        if not isinstance(g.get("inputs"), dict) or not all(entero(v) for v in g["inputs"].values()):
            fallo(p, "inputs debe contener versiones enteras positivas.")
        if not isinstance(g.get("outputs"), list) or not all(texto(x) for x in g["outputs"]):
            fallo(p, "outputs debe ser una lista de referencias.")
        rv = g.get("review")
        if rv is not None:
            if not (isinstance(rv, dict) and texto(rv.get("actor")) and texto(rv.get("source_ref"))
                    and entero(rv.get("version")) and rv.get("decision") in ("approve", "revise", "reject", "defer")):
                fallo(p, "review necesita actor, source_ref, version y decision válidos.")
        st = g.get("status")
        if st in ("ready_for_review", "approved") and not g.get("outputs"):
            fallo(p, "el paquete necesita outputs concretos antes de revisión o aprobación.")
        if st == "approved" and not (isinstance(rv, dict) and rv.get("decision") == "approve" and rv.get("version") == g.get("version")):
            fallo(p, "falta aprobación explícita de esta versión.")
        if st == "changes_requested" and not (isinstance(rv, dict) and rv.get("decision") in ("revise", "reject")
                                              and rv.get("version") == g.get("version")):
            fallo(p, "falta la revisión humana de esta versión.")
        if st == "not_applicable" and not no_aplica_permitido(estado, p):
            fallo(p, "solo H03_N (nombre conservado, o Exprés) y H01 (Exprés) pueden marcarse como no aplica.")

    if cps.get("H00", {}).get("status") in ("ready_for_review", "approved"):
        for k in ("id", "company", "objective", "approver"):
            if not texto(pr.get(k)):
                fallo("H00", f"falta project.{k}.")
        if alc.get("naming") == "undecided":
            fallo("H00", "decide el alcance del naming.")
        if not alc.get("deliverables"):
            fallo("H00", "faltan entregables en alcance.")
        if alc.get("naming") == "retain" and not texto(alc.get("existing_name")):
            fallo("H00", "identifica el nombre que se conserva.")

    for p in PUNTOS:
        g = cps.get(p)
        if not isinstance(g, dict):
            aceptado[p] = False
            continue
        pad = padres(estado, p)
        listo = g.get("status") in ("ready_for_review", "approved", "not_applicable")
        if listo and isinstance(g.get("inputs"), dict):
            if set(g["inputs"]) != set(pad):
                fallo(p, "inputs no coincide con las dependencias de este punto.")
            for q in pad:
                if not aceptado.get(q):
                    fallo(p, f"la dependencia {q} no está aceptada y vigente.")
                if g["inputs"].get(q) != cps.get(q, {}).get("version"):
                    fallo(p, f"versión consumida de {q} desactualizada.")
        aceptado[p] = (g.get("status") in ("approved", "not_applicable") and not locales[p]
                       and all(aceptado.get(q) for q in pad))

    valido = not errores
    r = {
        "valid": valido, "errors": errores,
        "accepted": [p for p in PUNTOS if aceptado.get(p)],
        "pending": [p for p in PUNTOS if not aceptado.get(p)],
        "can_start": [p for p in PUNTOS if valido and cps.get(p, {}).get("status") in ("draft", "changes_requested", "needs_review")
                      and all(aceptado.get(q) for q in padres(estado, p))],
    }
    if pedido:
        r["checkpoint"] = {"id": pedido, "accepted": valido and bool(aceptado.get(pedido))}
    return r


def cargar(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def guardar(ruta, estado):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)
        f.write("\n")


def historial(estado, punto, accion, ref=""):
    estado.setdefault("history", []).append({
        "date": hoy(), "checkpoint": punto, "action": accion,
        "version": estado["checkpoints"][punto]["version"] if punto in estado["checkpoints"] else None, "ref": ref,
    })


def aceptado_ahora(estado, punto):
    return punto in validar(estado)["accepted"]


def exigir_padres(estado, punto):
    falta = [q for q in padres(estado, punto) if not aceptado_ahora(estado, q)]
    if falta:
        sys.exit(f"{punto} depende de {', '.join(falta)}, que aún no está aceptado.")


def marcar_no_aplica(estado):
    """Tras aprobar H00: en Exprés, H01 y H03_N no aplican; en Completa, H03_N no aplica si se conserva el nombre."""
    cps = estado["checkpoints"]
    for p in ("H01", "H03_N"):
        if no_aplica_permitido(estado, p) and cps[p]["status"] in ("draft", "needs_review"):
            cps[p]["status"] = "not_applicable"
            cps[p]["inputs"] = {"H00": cps["H00"]["version"]}
            historial(estado, p, "no aplica", "según el alcance aprobado en H00")


def dependientes(estado, punto):
    """Puntos que dependen (directa o indirectamente) de `punto`, según las dependencias vigentes."""
    out, cola = set(), [punto]
    while cola:
        actual = cola.pop()
        for p in PUNTOS:
            if actual in padres(estado, p) and p not in out:
                out.add(p)
                cola.append(p)
    return [p for p in PUNTOS if p in out]


def cmd_init(a):
    estado = {
        "schema_version": 2,
        "project": {
            "id": a.id or a.empresa.lower().replace(" ", "-"), "company": a.empresa, "objective": a.objetivo,
            "approver": a.aprueba, "depth": a.profundidad,
            "scope": {"naming": a.naming, "existing_name": a.nombre_existente, "deliverables": a.entregable or []},
        },
        "evidence_register": None, "decision_register": None,
        "checkpoints": {p: {"version": 1, "status": "draft", "inputs": {}, "outputs": [], "review": None} for p in PUNTOS},
        "history": [], "pending": [], "maintenance": {"owner": None, "changes_need_approval": None},
    }
    guardar(a.estado, estado)
    print(f"✔ Estado creado en {a.estado} (profundidad {a.profundidad}).")


def cmd_alcance(a):
    estado = cargar(a.estado)
    alc = estado["project"]["scope"]
    if a.naming:
        alc["naming"] = a.naming
    if a.nombre_existente is not None:
        alc["existing_name"] = a.nombre_existente
    if a.entregable:
        alc["deliverables"] = a.entregable          # sustituye la lista entera
    for e in a.anadir_entregable or []:              # añade sin borrar (p. ej. banners en un kit ya hecho)
        if e not in alc.setdefault("deliverables", []):
            alc["deliverables"].append(e)
    if a.objetivo:
        estado["project"]["objective"] = a.objetivo
    guardar(a.estado, estado)
    print("✔ Alcance actualizado.")


def cmd_preparar(a):
    estado = cargar(a.estado)
    g = estado["checkpoints"][a.punto]
    exigir_padres(estado, a.punto)
    g["inputs"] = {q: estado["checkpoints"][q]["version"] for q in padres(estado, a.punto)}
    for s in a.salida:
        if s not in g["outputs"]:
            g["outputs"].append(s)
    g["status"] = "ready_for_review"
    historial(estado, a.punto, "listo para revisar", "; ".join(a.salida))
    guardar(a.estado, estado)
    print(f"✔ {a.punto} v{g['version']} listo para revisar.")


def cmd_aprobar(a):
    estado = cargar(a.estado)
    g = estado["checkpoints"][a.punto]
    if g["status"] != "ready_for_review":
        sys.exit(f"{a.punto} está en «{ETIQUETA[g['status']]}»: primero prepáralo (preparar) con su paquete.")
    exigir_padres(estado, a.punto)
    g["review"] = {"actor": a.actor, "source_ref": a.ref, "decision": "approve", "version": g["version"]}
    g["status"] = "approved"
    historial(estado, a.punto, "aprobado", a.ref)
    if a.punto == "H00":
        marcar_no_aplica(estado)
    guardar(a.estado, estado)
    r = validar(estado)
    print(f"✔ {a.punto} v{g['version']} aprobado. Se puede empezar: {', '.join(r['can_start']) or 'nada nuevo'}.")


def cmd_cambios(a):
    estado = cargar(a.estado)
    g = estado["checkpoints"][a.punto]
    g["review"] = {"actor": a.actor, "source_ref": a.ref, "decision": "revise", "version": g["version"]}
    g["status"] = "changes_requested"
    historial(estado, a.punto, "cambios pedidos: " + (a.nota or ""), a.ref)
    guardar(a.estado, estado)
    print(f"✔ {a.punto} v{g['version']}: cambios pedidos registrados.")


def cmd_nueva_version(a):
    estado = cargar(a.estado)
    g = estado["checkpoints"][a.punto]
    g["version"] += 1
    g["status"] = "draft"
    historial(estado, a.punto, "nueva versión: " + a.motivo)
    marcados = []
    for d in dependientes(estado, a.punto):
        gd = estado["checkpoints"][d]
        if gd["status"] in ("approved", "ready_for_review", "changes_requested", "not_applicable"):
            gd["status"] = "needs_review"
            marcados.append(d)
            historial(estado, d, f"pendiente de revisión por el cambio en {a.punto}")
    guardar(a.estado, estado)
    print(f"✔ {a.punto} pasa a v{g['version']} (borrador)." + (f" Revisar: {', '.join(marcados)}." if marcados else ""))


def cmd_pendiente(a):
    estado = cargar(a.estado)
    lista = estado.setdefault("pending", [])
    if a.hecho:
        i = a.hecho - 1
        if not 0 <= i < len(lista):
            sys.exit("Número de pendiente inexistente.")
        lista[i]["done"] = hoy()
        print(f"✔ Hecho: {lista[i]['text']}")
    else:
        lista.append({"text": a.texto, "added": hoy(), "done": None})
        print(f"✔ Pendiente {len(lista)}: {a.texto}")
    guardar(a.estado, estado)


def cmd_mantenimiento(a):
    estado = cargar(a.estado)
    m = estado.setdefault("maintenance", {})
    if a.responsable:
        m["owner"] = a.responsable
    if a.cambios:
        m["changes_need_approval"] = a.cambios
    guardar(a.estado, estado)
    print("✔ Mantenimiento actualizado.")


def cmd_validar(a):
    r = validar(cargar(a.estado), a.punto)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    sys.exit(1 if not r["valid"] else (2 if a.punto and not r["checkpoint"]["accepted"] else 0))


def cmd_md(a):
    estado = cargar(a.estado)
    pr, cps = estado["project"], estado["checkpoints"]
    prof = "Exprés" if pr.get("depth") == "expres" else "Completa"
    l = [f"# Decisiones y versiones", "",
         f"Proyecto de marca de **{pr.get('company')}** · profundidad {prof} · actualizado el {hoy()}.", "",
         "Este registro dice qué se aprobó, sobre qué versión y dónde, qué queda pendiente y quién mantiene el kit.", "",
         "## Puntos de validación", "", "| Punto | Qué se aprueba | Versión | Estado | Referencia |", "|---|---|---|---|---|"]
    for p in PUNTOS:
        g = cps[p]
        if pr.get("depth") == "expres" and p in ("H01", "H03_N") and g["status"] == "not_applicable":
            ref = "Exprés"
        else:
            ref = (g.get("review") or {}).get("source_ref", "—") if g["status"] in ("approved", "changes_requested") else "—"
        l.append(f"| {p} | {QUE[p]} | v{g['version']} | {ETIQUETA[g['status']]} | {ref} |")
    l += ["", "## Historial", ""]
    if estado.get("history"):
        l += ["| Fecha | Punto | Cambio | Versión | Referencia |", "|---|---|---|---|---|"]
        for h in estado["history"]:
            l.append(f"| {h['date']} | {h['checkpoint']} | {h['action']} | v{h.get('version') or '—'} | {h.get('ref') or '—'} |")
    else:
        l.append("Sin cambios registrados todavía.")
    l += ["", "## Pendientes y comprobaciones no hechas", ""]
    abiertos = [x for x in estado.get("pending", []) if not x.get("done")]
    cerrados = [x for x in estado.get("pending", []) if x.get("done")]
    l += [f"- {x['text']}" for x in abiertos] or ["- Ninguno."]
    if cerrados:
        l += ["", "Resueltos:"] + [f"- ~~{x['text']}~~ ({x['done']})" for x in cerrados]
    m = estado.get("maintenance", {})
    l += ["", "## Mantenimiento", "",
          f"- **Responsable del kit:** {m.get('owner') or 'por definir'}",
          f"- **Cambios que necesitan una nueva aprobación:** {m.get('changes_need_approval') or 'cambios en logo, color, tipografía o promesa de marca'}",
          ""]
    with open(a.salida, "w", encoding="utf-8") as f:
        f.write("\n".join(l))
    print(f"✔ {a.salida}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    i = sp.add_parser("init")
    i.add_argument("estado")
    i.add_argument("--empresa", required=True)
    i.add_argument("--objetivo", required=True)
    i.add_argument("--id")
    i.add_argument("--aprueba", default="usuario")
    i.add_argument("--profundidad", choices=["completa", "expres"], default="completa")
    i.add_argument("--naming", choices=sorted(NAMING), default="undecided")
    i.add_argument("--nombre-existente")
    i.add_argument("--entregable", action="append")
    al = sp.add_parser("alcance")
    al.add_argument("estado")
    al.add_argument("--naming", choices=sorted(NAMING))
    al.add_argument("--nombre-existente")
    al.add_argument("--entregable", action="append", help="sustituye la lista de entregables")
    al.add_argument("--anadir-entregable", action="append", help="añade un entregable a la lista")
    al.add_argument("--objetivo")
    for nombre in ("preparar", "aprobar", "cambios", "nueva-version"):
        s = sp.add_parser(nombre)
        s.add_argument("estado")
        s.add_argument("punto", choices=PUNTOS)
        if nombre == "preparar":
            s.add_argument("--salida", action="append", required=True)
        if nombre in ("aprobar", "cambios"):
            s.add_argument("--ref", required=True)
            s.add_argument("--actor", default="usuario")
        if nombre == "cambios":
            s.add_argument("--nota")
        if nombre == "nueva-version":
            s.add_argument("--motivo", required=True)
    pe = sp.add_parser("pendiente")
    pe.add_argument("estado")
    pe.add_argument("texto", nargs="?")
    pe.add_argument("--hecho", type=int)
    ma = sp.add_parser("mantenimiento")
    ma.add_argument("estado")
    ma.add_argument("--responsable")
    ma.add_argument("--cambios")
    v = sp.add_parser("validar")
    v.add_argument("estado")
    v.add_argument("--punto", choices=PUNTOS)
    m = sp.add_parser("md")
    m.add_argument("estado")
    m.add_argument("--salida", required=True)
    a = p.parse_args()
    {
        "init": cmd_init, "alcance": cmd_alcance, "preparar": cmd_preparar, "aprobar": cmd_aprobar,
        "cambios": cmd_cambios, "nueva-version": cmd_nueva_version, "pendiente": cmd_pendiente,
        "mantenimiento": cmd_mantenimiento, "validar": cmd_validar, "md": cmd_md,
    }[a.cmd](a)


if __name__ == "__main__":
    main()

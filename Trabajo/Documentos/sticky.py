# 1. SIN sticky (por defecto queda centrado)
# frame.grid(row=0, column=0)
# ┌─────────────┐
# │             │
# │    [Frame]  │
# │             │
# └─────────────┘
#
# 2. sticky="nsew" (se expande en todas direcciones)
# frame.grid(row=0, column=0, sticky="nsew")
# ┌─────────────┐
# │┌───────────┐│
# ││   Frame   ││
# │└───────────┘│
# └─────────────┘
#
# 3. sticky="n" (pegado arriba, centrado horizontalmente)
# frame.grid(row=0, column=0, sticky="n")
# ┌─────────────┐
# │   [Frame]   │
# │             │
# │             │
# └─────────────┘
#
# 4. sticky="w" (pegado a la izquierda, centrado verticalmente)
# frame.grid(row=0, column=0, sticky="w")
# ┌─────────────┐
# │[Frame]      │
# │             │
# └─────────────┘
#
# 5. sticky="e" (pegado a la derecha)
# frame.grid(row=0, column=0, sticky="e")
# ┌─────────────┐
# │      [Frame]│
# │             │
# └─────────────┘
#
# 6. sticky="ew" (se expande horizontalmente)
# frame.grid(row=0, column=0, sticky="ew")
# ┌─────────────┐
# │             │
# │┌───────────┐│
# │└───────────┘│
# └─────────────┘
#
# 7. sticky="ns" (se expande verticalmente)
# frame.grid(row=0, column=0, sticky="ns")
# ┌─────────────┐
# │┌─────────┐  │
# ││ Frame   │  │
# │└─────────┘  │
# └─────────────┘
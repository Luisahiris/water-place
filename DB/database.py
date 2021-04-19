# cultKc = {
#     ['tabaco']: [0.35, 0.75, 1.10, 0.90],
#     ['cacao']: [0.90, 0.90, 0.90, 0.90],
#     ['papa']: [0.45, 0.75, 1.15, 0.80],
#     ['remolacha']: [0.45, 0.80, 1.15, 0.80],
#     ['maiz']: [0.40, 0.80, 1.15, 0.70],
#     ['tomate']: [0.45, 0.75, 1.15, 0.80],
#     ['platano']: [0.45, 0.70, 1.10, 0.80],
#     ['arroz']: [1.05, 1.20, 0.75, 1.6]
# }

crops = {
  'remolacha': {
    'kc': { 'init': 0.45, 'dev': 0.80, 'mid': 1.15, 'end': 0.80},
    'days': { 'init': 15, 'dev': 25, 'mid': 20, 'end': 10, 'total': 70 }
  },
  'papa': {
    'kc': { 'init': 0.45, 'dev': 0.75, 'mid': 1.15, 'end': 0.80},
    'days': { 'init': 25, 'dev': 30, 'mid': 40, 'end': 30, 'total': 125 }
  }
}

cultivos = [
    'Papa',
    'Remolacha'
]

# riego = {
#     ['goteo']: [],
#     ['aspersión']: [],
#     ['gravedad']: [],
# }

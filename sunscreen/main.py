import argparse

import sunscreen.renderer

def main():
  print('From Main()')
  args = parse_args()
  renderer = sunscreen.renderer.Renderer(args.fullscreen)
  renderer.run()
  print('Quitting')

def parse_args():
  parser = argparse.ArgumentParser(
    prog='sunscreen',
    description='Displays stats from an enphase solar system.')
  parser.add_argument('-f', '--fullscreen', action='store_true')
  return parser.parse_args()

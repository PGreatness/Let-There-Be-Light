import math
from display import *

  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 2

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    amb = calculate_ambient(ambient,areflect)
    diff = calculate_diffuse(light,dreflect,normal)
    spec = calculate_specular(light,sreflect,view,normal)

    def sum(*args):
      totalSum = []
      for x in range(len(args[0])):
          currSum = 0
          for i in range(len(args)):
              currSum += args[i][x]
          totalSum.append(currSum)
      return totalSum

    color = sum(amb,diff,spec)
    limit_color(color)
    return color

def calculate_ambient(alight, areflect):
    return [alight[x] * areflect[x] for x in range(len(alight))]

def calculate_diffuse(light, dreflect, normal):
    loc, col = light
    normalize(loc)
    normalize(normal)
    norm = dot_product(loc, normal)
    return [dreflect[x] * col[x] * norm for x in range(len(dreflect))]

def calculate_specular(light, sreflect, view, normal):
    loc, col = light
    normalize(loc)
    normalize(normal)
    normalize(view)

    def subtract(a, b):
      return [a[x] - b[x] for x in range(len(a))]
    def distribute(a, b):
      return [a * x for x in b]

    norm = dot_product(subtract(distribute(2 * dot_product(loc, normal),normal), loc), view)
    norm = math.pow(abs(norm), SPECULAR_EXP) * norm / abs(norm)

    return [sreflect[x] * col[x] * norm for x in range(len(sreflect))]

def limit_color(color):
    for i in range(len(color)):
        a = color[i]
        color[i] = a if a <= 255 and a > 0 else 255 if a > 255 else 0
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N

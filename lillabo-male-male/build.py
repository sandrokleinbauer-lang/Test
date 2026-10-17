# Baut das FreeCAD-Dokument ohne Oberfläche und exportiert STEP und STL.
#   freecadcmd build.py
import os
import sys

import FreeCAD as App
import Import
import MeshPart

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import importlib.util

spec = importlib.util.spec_from_file_location("lmm", os.path.join(HERE, "lillabo_male_male.FCMacro"),
                                              loader=importlib.machinery.SourceFileLoader(
                                                  "lmm", os.path.join(HERE, "lillabo_male_male.FCMacro")))
lmm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lmm)

doc = App.newDocument("Lillabo_Stecker_Stecker")
objs = lmm.build(doc)
doc.saveAs(os.path.join(HERE, "Lillabo_Stecker_Stecker.FCStd"))

os.makedirs(os.path.join(HERE, "export"), exist_ok=True)
for name, (obj, shape) in objs.items():
    base = os.path.join(HERE, "export", name)
    tmp = doc.addObject("Part::Feature", name + "_export")
    tmp.Shape = shape
    Import.export([tmp], base + ".step")
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.01, AngularDeflection=0.0873, Relative=False)
    mesh.write(base + ".stl")
    doc.removeObject(tmp.Name)
    bb = shape.BoundBox
    print("%s: valid=%s solids=%d volume=%.1f mm3 box=%.1f x %.1f x %.1f mm, facets=%d"
          % (name, shape.isValid(), len(shape.Solids), shape.Volume, bb.XLength, bb.YLength, bb.ZLength,
             mesh.CountFacets))

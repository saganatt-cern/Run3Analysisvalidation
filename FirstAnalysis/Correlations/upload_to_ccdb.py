#!/usr/bin/env python
# coding: utf-8

import ROOT

import os as os
import datetime as dt

production = "LHC20f4a"

# input file with efficiency histograms extracted beforehand
inputfile = ROOT.TFile("efficiency.root", "read")

# create a TList out of the efficiency histograms from the input file
mylist = ROOT.TList()
mylist.SetName("efficiency_histograms")

histo = inputfile.Get("efficiency");

mylist.Add(histo)

# # Let's produce the CCDB object
ccdb_path = "Users/k/kgajdoso/efficiency"
#ccdb_url = "http://alice-ccdb.cern.ch:8080"
ccdb_url = "http://ccdb-test.cern.ch:8080"
metadata = ROOT.std.map(ROOT.std.string,ROOT.std.string)()

ccdb = ROOT.o2.ccdb.CcdbApi()
ccdb.init(ccdb_url)

# store the object to ccdb
def storeInCCDB(production,ccdblst) :
    dtnow = dt.datetime.now()
    sor = int(dt.datetime(dtnow.year,dtnow.month,dtnow.day,0,0,0,0,tzinfo=dt.timezone.utc).timestamp())*1000
    eor = int(dt.datetime(dtnow.year,dtnow.month,dtnow.day,23,59,59,0,tzinfo=dt.timezone.utc).timestamp())*1000
    metadata.insert(ROOT.std.pair(ROOT.std.string,ROOT.std.string)("Period","%s" % production))
    metadata.insert(ROOT.std.pair(ROOT.std.string,ROOT.std.string)("Date","%s" % dtnow.strftime('%Y%m%d')))
    ccdb.storeAsTFileAny[ROOT.TList](ccdblst,ccdb_path,metadata,int(sor),int(eor))

ccdblst = mylist
storeInCCDB(production,ccdblst)

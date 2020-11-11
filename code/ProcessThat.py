import csv
import requests
import os
import glob

# generate random integer values
from numpy.random import seed
from numpy.random import randint
import numpy as np

#import parseArgs

import sys


def coinFlip(p):    
    #perform the binomial distribution (returns 0 or 1)    
    result = np.random.binomial(1,p) 
       
    #return flip to be added to numpy array    
    return result


class ProcessThat:
   """
      Defines a class to interact with the Stocks object.
   """

   def __init__( self, userArgs=None ):
      """
         Initialization args.
      """

      self.symbolFile = "MiniMe.csv"

      self.dataDirectory = './data/'

      self.sampleExtension = 'at'

      # seed random number generator
      seed(42)


   def cleanup( self ):
      """
         Perform cleanup as required.
      """
      

   def getSymbols( self, symbolFile='MiniMe.csv' ):
      """
         Read a .csv file of symbols.
      """

      # TODO: Move this to finnhub-data repo.

      with open(symbolFile, 'r', newline='') as csvfile:
         data = list(csv.reader(csvfile))

         # The first line contains the header row.  Delete it.
         data.pop(0)

         symbols = []
         for symbol_info in data:
            symbols.append( symbol_info[0] )

         return symbols

   def pause(self):
         input("Press the <ENTER> key to continue...")

   def getCsvFileNames(self):
      """
         @brief Get a list of CSV file names in the form of <symbol>.csv

         @return A list of valid CSV file names.
      """

      # Updated
      csvFileNames = []
      symbols = self.getSymbols(self.symbolFile)

      for symbol in symbols:
         csvFileNames.append(f'./data/{symbol}.csv')

      return csvFileNames, symbols

   def combineTotalFiles(self, createTotalFiles=False):
      """
         @brief There is a total file for each stock.  This method concatenates them.
         @return An array containing the concatenated files.
      """

      np.random.seed(42)


      dataType = 'Total'
      symbols = self.getSymbols(self.symbolFile)

      xPaths = []
      yPaths = []

      for symbol in symbols:
         xPath = f'{self.dataDirectory}X{dataType}{symbol}.{self.sampleExtension}'
         yPath = f'{self.dataDirectory}Y{dataType}{symbol}.{self.sampleExtension}'

         xPaths.append(xPath)
         yPaths.append(yPath)

      xPathOutTrain = f'{self.dataDirectory}XTrain.{self.sampleExtension}'
      yPathOutTrain = f'{self.dataDirectory}YTrain.{self.sampleExtension}'

      xPathOutDev = f'{self.dataDirectory}XDev.{self.sampleExtension}'
      yPathOutDev = f'{self.dataDirectory}YDev.{self.sampleExtension}'

      xPathOutTest = f'{self.dataDirectory}XTest.{self.sampleExtension}'
      yPathOutTest = f'{self.dataDirectory}YTest.{self.sampleExtension}'

      yWrites = []

      if createTotalFiles:
         filenamesX = xPaths
         with open(xPathOutTrain, 'w') as outfileTrain:
          with open(xPathOutDev, 'w') as outfileDev:
           with open(xPathOutTest, 'w') as outfileTest:
            for fname in filenamesX:
               print(fname)
               with open(fname) as infile:
                  for line in infile:
                     if coinFlip(.02):
                        outfileDev.write(line)
                        yWrites.append('dev')
                     elif coinFlip(.02):
                        outfileTest.write(line)
                        yWrites.append('test')
                     else:
                        outfileTrain.write(line)
                        yWrites.append('train')

         yIndex = 0
         filenamesY = yPaths
         with open(yPathOutTrain, 'w') as outfileTrain:
          with open(yPathOutDev, 'w') as outfileDev:
           with open(yPathOutTest, 'w') as outfileTest:
            for fname in filenamesY:
               print(fname)
               with open(fname) as infile:
                  for line in infile:
                     if 'train' == yWrites[yIndex]:
                        outfileTrain.write(line)
                     elif 'dev' == yWrites[yIndex]:
                        outfileDev.write(line)
                     else:
                        outfileTest.write(line)

                     yIndex += 1


      return 1, 2


   def main( self, userArgs=None ):
      """
         @brief Main code of the object.
      """

      # Processing 50 stocks!!!

      combineTotalFiles = True

      if combineTotalFiles:
         [xTotal, yTotal] = self.combineTotalFiles(createTotalFiles=True)

      return 0


def execMain( userArgs=None ):
   """
      Main code.
   """

   pt = ProcessThat( )

   exitValue = pt.main()

   pt.cleanup()

   return exitValue

if __name__ == '__main__':
    try:
        retVal = execMain()
    except KeyboardInterrupt:
        print('Received <Ctrl>+c')
        sys.exit(-1)

    sys.exit(retVal)


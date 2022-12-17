
import unittest
import windpressurezones
import json


file = open("data.json")
data = file.read()
file.close()

parsedJson = json.loads(data)
data = parsedJson["FACE"]


class test_windpressurezones(unittest.TestCase):


    
    def test_length(self):

        line = data[0]["POLYGON"]["@path"]["L1"]
        result = round(windpressurezones.length(line),5)
        answer = round(37.720000450001,5)
        self.assertEqual(result,answer)
        


    def test_length_between2_points(self):

       
        result = round(windpressurezones.length_between2_points(1,1,0,5,5,0),5)
        answer = round(5.6568542494924,5)
        self.assertEqual(result,answer)

    def test_new_coordinates_in_line(self):

        a = 10
        line = data[0]["POLYGON"]["@path"]["L1"]
        r1,r2,r3,r4,r5,r6 = windpressurezones.new_coordinates_in_line(line,a,37.720000450001)

        self.assertEqual(round(r1,5),3.45236)
        self.assertEqual(round(r2,5),27.50417)
        self.assertEqual(round(r3,5),29.53795)
        self.assertEqual(round(r4,5),1.24544)
        self.assertEqual(round(r5,5),9.92214)
        self.assertEqual(round(r6,5),29.53795)


    def test_add_the_vectors(self):

        r1,r2,r3 = windpressurezones.add_the_vectors(-1,2,3,-3,2,4)
        self.assertEqual(r1,-4)
        self.assertEqual(r2,4)
        self.assertEqual(r3,7)

    def test_get_the_vector(self):

        r1,r2,r3 = windpressurezones.get_the_vector(-1,2,3,-3,2,4)
        self.assertEqual(r1,2)
        self.assertEqual(r2,0)
        self.assertEqual(r3,-1)


if __name__ == "__main__":

    unittest.main()


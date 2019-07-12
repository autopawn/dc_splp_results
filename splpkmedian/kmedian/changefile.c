#include <fstream>
#include <iostream>
#include <cstdlib>
#include <cstdio>
#include <cmath>
using namespace std;

double numberize(ifstream& eingabe)
{
  char c;
  int nach = 0;
  double number = 0;
  bool negative, after;

  negative = after = false;
  
  // Pass SPACE-characters
  while (((c = eingabe.get()) == ' ') || (c == '\n'));

  // Read double-type number from input-stream
  if (c == '-') negative = true;
  while((c != ' ') && 
	(c != '\n') && 
	(!eingabe.eof())) {
    if (c == '.') after = true;
    else if ((c < 48) || (c > 57)) number = -1; //return;
    else {
      //  cout << c;
      number = (number * 10) + (c - 48);
      if (after) nach++;
    }
    c = eingabe.get();
  }

  number = number * pow((double)10,(double)(-nach));
  if (negative) number = -number;
  return number;
}


void term()
{
  cout << "changefile [DENOM] [SOURCEFILE] [TARGETFILE] \n " \
  "DENOM integer please !\n ";
  exit(0);
}


int main(int argc, char** argv) 
{
  int i,j,facilities, cities;
  if (argc < 4) term();
  
  int denom = atoi(argv[1]);

  ifstream eingabe(argv[2], ios::in);
  ofstream ausgabe(argv[3], ios::out);

  if ((!eingabe.good()) || (!ausgabe.good())) term();
  
  double help;
  char zeile[250];
  eingabe.getline(zeile, 250); // Read 'FILE:'
  ausgabe << "FILE: " << argv[3] << endl;
  
  facilities = (int) numberize(eingabe);
  cities = (int) numberize(eingabe);
  help = numberize(eingabe);

  ausgabe << facilities << " " << cities << " 0 " << endl;
  
  // Ready reading number of facilities and cities
  
  double *open_cost = new double [facilities];
  
  int facil = 0;
  
  i = 0;
  while (i < facilities) {
    
    facil = (int) numberize(eingabe);
    open_cost[facil-1] = numberize(eingabe);

    ausgabe << facil << " " << ((int) (0.5 + (double) open_cost[facil-1] / denom)) << " ";

    facil--;
    j = 0;
    while (j < cities) {
      ausgabe << numberize(eingabe) << " ";
      j++;
    }
    ausgabe << endl;
    i++;
  } // end while (i < facilities)
  
  // Ready reading opening and connection costs
  
  ausgabe.close();
  eingabe.close();
}
 

/*****************************************************************************
* 
*  Author: Carlos Moreno
*          July 2017
* 
*  This program splits / de-interleaves the two channels, saving to 
*  files with filename suffixed channel-A, channel-B
* 
*****************************************************************************/

#include <iostream>
#include <iomanip>
#include <string>
#include <fstream>
#include <cstdio>
#include <cstdlib>
#include <inttypes.h>

using namespace std;

void usage (const char * arg[])
{
    cout << "ERROR -- Usage: " << arg[0] << " <bin file>" << endl;
}

int main(int argc, const char * arg[])
{
    const int mandatory_arguments = 2;
    const int arg_filename = 1;

    if (argc < mandatory_arguments)
    {
        usage (arg);
        return 1;
    }

    const string filename (arg[arg_filename]);
    const string & output_file1 = filename + "--channel-A";
    const string & output_file2 = filename + "--channel-B";

    const int samples_per_buffer = 2048000;

    uint16_t data[2*samples_per_buffer];
    ifstream file(filename.c_str());

    ofstream output1 (output_file1.c_str());
    ofstream output2 (output_file2.c_str());

    while(file.read (reinterpret_cast<char *> (data), sizeof(data)))
    {
        output1.write (reinterpret_cast<char *>(data), samples_per_buffer * sizeof(uint16_t));
        output2.write (reinterpret_cast<char *>(data+samples_per_buffer), samples_per_buffer * sizeof(uint16_t));
    }

    return 0;
}

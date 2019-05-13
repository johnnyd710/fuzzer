/*****************************************************************************
* 
*  Author: Carlos Moreno
*          July 2017
* 
*  This program decodes single-channel binary files.  If multiple 
*  channels are captured, the binary file interleaves chunks of 
*  the two channels, which requires a decoding program that 
*  de-interleaves and saves to two separate files
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
    cout << "ERROR -- Usage: " << arg[0] << " <num channels -- 1 or 2> <bin file> <sampling rate (in MSPS)> [scale (200mV, 400mV, 800mV or 2V)]" << endl;
}

int main(int argc, const char * arg[])
{
    const int mandatory_arguments = 4;
    const int arg_num_channels = 1;
    const int arg_filename = 2;
    const int arg_sampling_rate = 3;
    const int arg_scale = 4;

    if (argc < mandatory_arguments)
    {
        usage (arg);
        return 1;
    }

    const int num_channels = atoi(arg[arg_num_channels]);
    if (num_channels != 1 && num_channels != 2)
    {
        cout << "Invalid parameter num channels = " << num_channels << " --- must be 1 or 2.\n\n";
        usage (arg);
        return 1;
    }

    int range_mV = 2000;
    if (argc == mandatory_arguments + 1)
    {
        const string rng (arg[arg_scale]);
        if (rng != "200mV" && rng != "400mV" && rng != "800mV" && rng != "2V") 
        {
            usage (arg);
            return 1;
        }
        range_mV = atoi(arg[arg_scale]);
        if (range_mV == 2) range_mV = 2000;
    }

    string filename (arg[arg_filename]);
    string output_file1, output_file2;
    
    if (num_channels == 1)
    {
        output_file1 = filename + ".txt";
        output_file2 = "/dev/null";
    }
    else
    {
        output_file1 = filename + "--channel-A.txt";
        output_file2 = filename + "--channel-B.txt";
    }

    const double sampling_rate = atoi(arg[arg_sampling_rate]) * 1000000;

    const int samples_per_buffer = 2048000;

    uint16_t data[samples_per_buffer];
    ifstream file(filename.c_str());

    ofstream output1 (output_file1.c_str());
    ofstream output2 (output_file2.c_str());

    uint64_t block = 0;
    while(file.read(reinterpret_cast<char *> (data), sizeof(data)))
    {
        ofstream & output = ((num_channels == 1) || ((num_channels == 2) && (block % 2 == 0))) ? output1 : output2;

        for (int k = 0; k < samples_per_buffer; ++k)
        {
            const uint64_t t = (block / num_channels) * samples_per_buffer + k;
                // time index --- if one channel, it just increases; if multiple channels, 
                // then every num_ch blocks the time indexes repeat (the samples of every 
                // num_ch blocks correspond to the same time indexes)

            output << fixed << setprecision(10) << (t / sampling_rate) << " ";
            if (argc == mandatory_arguments + 1)
            {
                output << static_cast<double>(data[k] - 32768) * range_mV / 32768.0 << endl;
            }
            else
            {
                output << (data[k] - 32768) << endl;
            }
        }
        ++block;
    }

    return 0;
}

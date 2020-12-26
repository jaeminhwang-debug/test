#include <iostream>
#include <fstream>
#include <math.h>

using namespace std;

// Sample data structure
#pragma pack(push, 1)
typedef struct {
    unsigned long long t : 20;
    unsigned long long a : 7;
    unsigned long long b : 9;
    unsigned long long c : 13;
    unsigned long long d : 15;
} BinStructure;
#pragma pack(pop)

// Make samples
void MakeSamples(BinStructure* out, unsigned int num) {
    const double PI = 3.14159265359;
    
    memset(out, 0, sizeof(BinStructure) * num);
    for(unsigned int i = 0; i < num; i++) {
        out[i].t = i;
        out[i].a = out[i].t;
        out[i].b = out[i].t;
        out[i].c = 4000 * (sin(2.0 * PI * 0.01 * out[i].t) + 1.0);
        out[i].d = 16000 * (cos(2.0 * PI * 0.01 * out[i].t) + 1.0);
    }
}

int main() {
    
    // Make samples
    unsigned int sampleNum = 1000;
    cout << "Making " << sampleNum << " samples" << endl;
    cout << "Element's size is " << sizeof(BinStructure) << " bytes" << endl;
    BinStructure* buf = new BinStructure[sampleNum];
    MakeSamples(buf, sampleNum);
    
    // Write
    ofstream ofs;
    const char* FNAME = "sample.bin";
    ofs.open(FNAME, ios::binary | ios::out);
    if (ofs.is_open()) {
        ofs.write(reinterpret_cast<char*>(buf), sizeof(BinStructure) * sampleNum);
        ofs.close();
        cout << FNAME << " generated" << endl;
    }

    delete [] buf;
    return 0;
}
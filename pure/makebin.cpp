#include <iostream>
#include <fstream>

using namespace std;

// Sample data structure
#pragma pack(push, 1)
typedef struct {
    unsigned int use22bits : 22;
    unsigned int use10bits : 10;

    unsigned short : 7;
    unsigned short use2bits : 2;
    unsigned short : 4;
    unsigned short use3bits : 3;
} BinStructure;
#pragma pack(pop)

// Make samples
void MakeSamples( BinStructure* out, unsigned int num ) {
    for( unsigned int i = 0; i < num; i++ ) {
        memset( &out[ i ], 0, sizeof( BinStructure ) );
        out[ i ].use22bits = out[ i ].use10bits = i;
        out[ i ].use2bits = out[ i ].use3bits = i;
    }
}

int main() {
    
    // Make samples
    unsigned int sampleNum = 10;
    cout << "Making " << sampleNum << " samples" << endl;
    BinStructure* buf = new BinStructure[ sampleNum ];
    MakeSamples( buf, sampleNum );
    
    // Write
    ofstream ofs;
    const char* FNAME = "sample.bin";
    ofs.open( FNAME, ios::binary | ios::out );
    if( ofs.is_open() ) {
        ofs.write( reinterpret_cast< char* >( buf ), sizeof( BinStructure ) * sampleNum );
        ofs.close();
        cout << FNAME << " generated." << endl;
    }

    delete [] buf;
    return 0;
}
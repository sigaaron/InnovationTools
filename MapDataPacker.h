/*
zinan@outlook.com

�򵥵�ѹ���㷨���Ѵ����ظ����ڴ����ݽ���һЩѹ��
*/

#ifndef MAPDATAPACKER_H
#define MAPDATAPACKER_H
#include <string>

typedef unsigned char * uchar_ptr;
typedef unsigned char  uchar;

#pragma pack(push) 
#pragma pack(1)
struct ZipHeader {
	size_t total;
	size_t nodes;
};

struct ZipNode {
	size_t count;
	uchar   c;
};
#pragma pack(pop)



class MapDataPacker
{
public:
	MapDataPacker();
	~MapDataPacker();

	int load_file_data(std::string file,uchar_ptr &data,size_t &len);
	int write_to_file(std::string file,uchar_ptr data, size_t len);
	//est�Ƿ�Ҫ�����С��������Ļ����뱣֤rdata���㹻��
	int zip(uchar_ptr data, size_t len, uchar_ptr &rdata, size_t &rlen,bool est = true);
	int unzip(uchar_ptr data, size_t len, uchar_ptr &rdata, size_t &rlen,bool est = true);
};


#endif

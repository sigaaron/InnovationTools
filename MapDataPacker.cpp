#include "pch.h"
#include "MapDataPacker.h"
#include <iostream>
#include <istream>
#include <ostream>
#include <fstream>

using namespace std;

MapDataPacker::MapDataPacker(){
}


MapDataPacker::~MapDataPacker(){
}


int MapDataPacker::load_file_data(std::string fname, uchar_ptr &data, size_t &len) {

	ifstream file(fname, ios::in | ios::binary);
	if (!file.is_open()) {
		return -2;
	}

	file.seekg(0, ios::end);
	len = file.tellg();

	file.seekg(0, ios::beg);

	data = new uchar[len];
	if (!data) {
		file.close();
		return -1;
	}

	file.read((char*)data, len);
	file.close();

	return 0;
}

int MapDataPacker::write_to_file(std::string fname, uchar_ptr data, size_t len) {
	ofstream ofile(fname, ios::out | ios::binary);

	if (!ofile.is_open()) {
		return -1;
	}

	ofile.write((char*)data, len);

	ofile.close();
	return 0;
}

int MapDataPacker::zip(uchar_ptr data, size_t len, uchar_ptr &rdata, size_t &rlen, bool est) {
	//先估算一下压缩后的数据量有多大

	ZipNode z = { 0 };
	size_t node_cnt = 0;
	size_t buff_sz = 0;
	if (est) {
		for (size_t s = 0; s < len; s++) {
			if (0 == s) {
				node_cnt++;
				z.c = data[s];
			}
			else {
				if (z.c != data[s]) {
					node_cnt++;
					z.c = data[s];
				}
			}
		}

		buff_sz = sizeof(ZipHeader) + node_cnt * sizeof(ZipNode);
		rdata = new uchar[buff_sz];
		if (!rdata) {
			return -1;
		}
		rlen = buff_sz;
	}
	memset(rdata, 0, rlen);

	ZipNode* tmp = (ZipNode*) (rdata + sizeof(ZipHeader));

	//-
	size_t inode = 0;
	ZipNode *pz = NULL;

	for (size_t s = 0; s < len; s++){
		if (0 == s) {
			pz = &tmp[inode];
			pz->c = data[s];
			pz->count++;
		}
		else {
			if (pz->c != data[s]) {
				pz = &tmp[++inode];
				pz->c = data[s];
				pz->count++;
			}
			else {
				pz->count++;
			}
		}
	}//for

	//出错了
	if (inode != node_cnt) {
		printf("warning: processing error\n");
	}
	else {
		printf("end: processing sucess\n");
	}

	//-ret
	ZipHeader * hdr = (ZipHeader*)rdata;
	hdr->total = len;//原始长度
	hdr->nodes = inode;//节点个数

	return 0;
}
int MapDataPacker::unzip(uchar_ptr data, size_t len, uchar_ptr &rdata, size_t &rlen,bool est) {
	
	ZipHeader * hdr = (ZipHeader*)data;
	if (est) {
		rdata = new uchar[hdr->total];
		if (!rdata) {
			return -1;
		}
		rlen = hdr->total;
	}
	//else--数据必须保证够用--
	size_t remain_len = rlen;

	uchar_ptr d = rdata;
	ZipNode * z = (ZipNode *)(data + sizeof(ZipHeader));
	for (size_t c = 0; c < hdr->nodes; c++) {
		ZipNode *node = &z[c];

		if (node->count > remain_len) {
			std::cout << "bad data" << std::endl;
			delete[] rdata;
			rdata = NULL;
			rlen = 0;

			return -2;
		}

		memset(d, node->c, node->count);
		d += node->count;
		remain_len -= node->count;
	}

	return 0;
}
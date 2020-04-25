#pragma once

#ifndef COLORCORRECT_CUTIL_CUTIL_H_
#define COLORCORRECT_CUTIL_CUTIL_H_
#endif
#include <stdlib.h>

typedef struct {
  int width;
  int height;
  unsigned char *r;
  unsigned char *g;
  unsigned char *b;
} rgbimage_t;

void calc_ace(rgbimage_t*, int, double, double);

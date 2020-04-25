#include "cutil.hpp"
#include <vector>
#include <math.h>
#include <cfloat>
#include <time.h>
#include <map>
#include <stdio.h>

typedef std::vector<double> doubleary;
typedef std::pair<int,int> intpair;
typedef std::vector<intpair> coordary;

typedef struct {
  doubleary *rary;
  doubleary *gary;
  doubleary *bary;
  double rsum;
  double gsum;
  double bsum;
  doubleary *ravgary;
  doubleary *gavgary;
  doubleary *bavgary;
} std_t;

typedef struct {
  double **rary;
  double **gary;
  double **bary;
  double rmax;
  double gmax;
  double bmax;
  double rmin;
  double gmin;
  double bmin;
} rscore_t;
double** new_2d_mat(rgbimage_t* img);
void delete_2d_mat(double** mat,rgbimage_t* img);
double calc_euclidean(int ax, int ay, int bx, int by);
double calc_saturation(int diff,double slope,double limit);
unsigned char linear_scaling(double r, double max, double min);
int get_pixel(unsigned char* ary,rgbimage_t* img, int x, int y);
void set_pixel(unsigned char* ary,rgbimage_t* img, int x, int y,unsigned char c);
rscore_t* create_rscore(rgbimage_t* img);
void delete_rsocre(rscore_t* rs,rgbimage_t* img);

coordary create_random_pair(int size, int x,int y);
void calc_ace(rgbimage_t* img, int samples, double slope, double limit);
void PyInit__cutil();

void PyInit__cutil(){
}

void calc_ace(rgbimage_t* img,int samples,double slope, double limit){
  srand((unsigned) time(NULL));
  coordary cary = create_random_pair(samples,img->width,img->height);
  rscore_t* rs = create_rscore(img);
  //Chromatic/Spatial Adjustment
  for(int i=0;i<img->height;++i){
    for(int j=0;j<img->width;++j){
      int r_pixel = get_pixel(img->r,img,j,i);
      int g_pixel = get_pixel(img->g,img,j,i);
      int b_pixel = get_pixel(img->b,img,j,i);
      double r_rscore_sum = 0.0;
      double g_rscore_sum = 0.0;
      double b_rscore_sum = 0.0;
      double denominator = 0.0;
      //calcurate r score from whole image
      //if you want accelerate the computation, use neighborhood pixels or random sampling insted of whole image.
      for(coordary::iterator it = cary.begin();it!=cary.end();it++){
        int l = it->first;
        int k = it->second;
        //if(k==i&&l==j)continue;
        /*
        if(k<i+(img->height/5)&&k>i-(img->height/5)){
          if(l<j+(img->width/5)&&l>j-(img->width/5)){
            continue;
          }
        }
        */
        double dist = calc_euclidean(j,i,l,k);
        if(dist<img->height/5)continue;
        r_rscore_sum += calc_saturation(r_pixel - get_pixel(img->r,img,l,k),slope,limit)/dist;
        g_rscore_sum += calc_saturation(g_pixel - get_pixel(img->g,img,l,k),slope,limit)/dist;
        b_rscore_sum += calc_saturation(b_pixel - get_pixel(img->b,img,l,k),slope,limit)/dist;
        denominator += limit/dist;
      }
      r_rscore_sum = r_rscore_sum/denominator;
      g_rscore_sum = g_rscore_sum/denominator;
      b_rscore_sum = b_rscore_sum/denominator;
      rs->rary[j][i]=r_rscore_sum;
      rs->gary[j][i]=g_rscore_sum;
      rs->bary[j][i]=b_rscore_sum;
      if(r_rscore_sum > rs->rmax)
        rs->rmax = r_rscore_sum;
      if(g_rscore_sum > rs->gmax)
        rs->gmax = g_rscore_sum;
      if(b_rscore_sum > rs->bmax)
        rs->bmax = b_rscore_sum;
      if(r_rscore_sum < rs->rmin)
        rs->rmin = r_rscore_sum;
      if(g_rscore_sum < rs->gmin)
        rs->gmin = g_rscore_sum;
      if(b_rscore_sum < rs->bmin)
        rs->bmin = b_rscore_sum;
    }
  }

  //Dynamic Tone Reproduction Scaling
  for(int i=0;i<img->height;++i){
    for(int j=0;j<img->width;++j){
      //scaling
      img->r[i*img->width+j]=linear_scaling(rs->rary[j][i],rs->rmax,rs->rmin);
      img->g[i*img->width+j]=linear_scaling(rs->gary[j][i],rs->gmax,rs->gmin);
      img->b[i*img->width+j]=linear_scaling(rs->bary[j][i],rs->bmax,rs->bmin);
    }
  }
  delete_rsocre(rs,img);
}
rscore_t* create_rscore(rgbimage_t* img){
  rscore_t* rs = new rscore_t;
  rs->rary = new_2d_mat(img);
  rs->gary = new_2d_mat(img);
  rs->bary = new_2d_mat(img);
  rs->rmax = DBL_MIN;
  rs->gmax = DBL_MIN;
  rs->bmax = DBL_MIN;
  rs->rmin = DBL_MAX;
  rs->gmin = DBL_MAX;
  rs->bmin = DBL_MAX;
  return rs;
}

void delete_rsocre(rscore_t* rs,rgbimage_t* img){
  delete_2d_mat(rs->rary,img);
  delete_2d_mat(rs->gary,img);
  delete_2d_mat(rs->bary,img);
  delete rs;
}

double** new_2d_mat(rgbimage_t* img){
  double** mat = new double*[img->width];
  for(int i=0; i<img->width; ++i){
    mat[i] = new double[img->height]();
  }
  return mat;
}

void delete_2d_mat(double** mat,rgbimage_t* img){
  for(int i = 0;i< img->width;++i){
    delete[] mat[i];
  }
  delete[] mat;
}

double calc_euclidean(int ax, int ay, int bx, int by){
  return sqrt(pow(ax-bx,2.0)+pow(ay-by,2.0));
}

double calc_saturation(int diff,double slope,double limit){
  double ret = diff*slope;
  if(ret>limit){
    return limit;
  }else if(ret < (-limit)){
    return  -limit;
  }else{
    return ret;
  }
}

int get_pixel(unsigned char* ary,rgbimage_t* img, int x, int y){
  return (int)ary[y*img->width+x];
}

void set_pixel(unsigned char* ary,rgbimage_t* img, int x, int y,unsigned char c){
  ary[y*img->width+x]=c;
}


unsigned char linear_scaling(double r, double max, double min){
  double slope = 255.0/(max - min);
  return (unsigned char)((r-min)*slope);
}

coordary create_random_pair(int size, int x,int y){
  coordary ret;
  for(int i=0;i<size;++i){
    int ranx = rand()%x;
    int rany = rand()%y;
    ret.push_back(intpair(ranx,rany));
  }

  return ret;
}
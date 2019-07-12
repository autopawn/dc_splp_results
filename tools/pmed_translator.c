#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <assert.h>

int main(int argc, char const *argv[]){
    if(argc!=3){
        fprintf(stderr,"usage: %s <input> <output>\n",argv[0]);
        exit(1);
    }
    // Read input file
    FILE *in_f = fopen(argv[1],"r");
    if(in_f==NULL){
        fprintf(stderr,"ERROR: couldn't open file \"%s\"!\n",argv[1]);
        exit(1);
    }
    int n_verts,n_edges,p;
    if(fscanf(in_f,"%d %d %d",&n_verts,&n_edges,&p)!=3){
        fprintf(stderr,"ERROR: could not read 3 first values.\n");
        exit(1);
    }
    // Set initial cost matrix
    int *costs = malloc(sizeof(int)*n_verts*n_verts);
    for(int i=0;i<n_verts;i++){
        for(int j=0;j<n_verts;j++){
            costs[n_verts*i+j] = INT_MAX/2;
        }
        costs[n_verts*i+i] = 0;
    }
    // Read edges
    for(int k=0;k<n_edges;k++){
        int i,j,cost;
        if(fscanf(in_f,"%d %d %d",&i,&j,&cost)!=3){
            fprintf(stderr,"ERROR: could not read edge.\n");
            exit(1);
        }
        i--; j--;
        assert(0<=i && i<n_verts);
        assert(0<=j && j<n_verts);
        costs[n_verts*i+j] = cost;
        costs[n_verts*j+i] = cost;
    }
    // Close file
    fclose(in_f);
    // Apply Floyd-Warshall
    for(int k=0;k<n_verts;k++){
        for(int i=0;i<n_verts;i++){
            for(int j=0;j<n_verts;j++){
                int old = costs[n_verts*i+j];
                int new = costs[n_verts*i+k]+costs[n_verts*k+j];
                if(new<old){
                    costs[n_verts*j+i] = new;
                    costs[n_verts*i+j] = new;
                }
            }
        }
    }
    // Write output file
    FILE *out_f = fopen(argv[2],"w");
    if(out_f==NULL){
        fprintf(stderr,"ERROR: couldn't open file \"%s\"!\n",argv[2]);
        exit(1);
    }
    fprintf(out_f,"FILE: %s\n",argv[2]);
    fprintf(out_f,"%d %d %d\n",n_verts,n_verts,p);
    for(int i=0;i<n_verts;i++){
        fprintf(out_f,"%d %d",i+1,0);
        for(int j=0;j<n_verts;j++){
            fprintf(out_f," %d",costs[n_verts*i+j]);
        }
        fprintf(out_f,"\n");
    }
    fclose(out_f);
    //
    free(costs);
    return 0;
}

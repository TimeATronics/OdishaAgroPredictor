""" 
 * This file is part of the OdishaAgroPredictor distribution (https://github.com/TimeATronics/OdishaAgroPredictor).
 * Citation:
 * Srivastava et al. A. K. Srivastava, M. Rajeevan, S. R. Kshirsagar : 
 * Development of High Resolution Daily Gridded Temperature Data Set (1969-2005) for the Indian Region.
 * ATMOSPHERIC SCIENCE LETTERS Atmos. Sci. Let. (2009) DOI: 10.1002/asl.232. 
"""
/* This program reads binary data for 365/366 days and writes in ascii file. */
#include <stdio.h>
#include <stdlib.h>
main()
{ float t[31][31];
int i,j ,k;
FILE *fin,*fout;
fin = fopen("C:\\Users\\AradhyaPC\\Downloads\\Maxtemp_MaxT_1970.GRD","rb"); // Input file
fout = fopen("1970.txt","w"); // Output file
fprintf(fout,"Daily Tempereture for 1970\n");
if(fin == NULL)
{ printf("Can't open file");
return 0;
}
if(fout == NULL)
{ printf("Can't open file");
return 0;
}
for(k=0 ; k<366 ; k++)
{ fread(&t,sizeof(t),1,fin) ;
if(k == 105)
{ for(i=0 ; i < 31 ; i++)
{ fprintf(fout,"\n") ;
for(j=0 ; j < 31 ; j++)
fprintf(fout,"%6.2f",t[i][j]);
}
}
}
fclose(fin);
fclose(fout);
return 0;
} /* end of main */
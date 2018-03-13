fid = fopen('Imagelist.txt','w');
for i=1:15000
    fprintf(fid,'%05d\n',i-1);
end
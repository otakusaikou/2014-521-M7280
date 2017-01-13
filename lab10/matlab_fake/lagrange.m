function lg=lagrange(x,y,lp)
n=length(x);
a=0;
   for i=1:n    
       p=1;
       q=1;
       for j=1:n
         if (i~=j)
            p=p*(lp-x(j));
            q=q*(x(i)-x(j));
         end
       end
      a=a+(p/q)*y(i);
   end
lg=a;
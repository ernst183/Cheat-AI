Fish = csvread('owl_vs_fish_ppst.txt');
for i=1:21
    Fish(i,4)=Fish(i,4)/(Fish(i,4)+Fish(i,5));
end
Frog = csvread('owl_vs_frog_ppst.txt');
for i=1:21
    Frog (i,4)=Frog (i,4)/(Frog (i,4)+Frog (i,5));
end
Eel = csvread('owl_vs_eel_ppst.txt');
for i=1:21
    Eel(i,4)=Eel(i,4)/(Eel(i,4)+Eel(i,5));
end
Sala = csvread('owl_vs_salamander_ppst.txt');
for i=1:21
    Sala(i,4)=Sala(i,4)/(Sala(i,4)+Sala(i,5));
end


plot(Fish(:,1),Fish(:,4),'b','LineWidth',2);
hold on;
plot(Frog(:,1),Frog(:,4),'r','LineWidth',2);
plot(Eel(:,1),Eel(:,4),'g','LineWidth',2);
plot(Sala(:,1),Sala(:,4),'k','LineWidth',2);


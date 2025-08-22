---
author: jimioke
title: "Nice Gantt charts in LaTeX"
date: 2024-06-18T11:50:53-05:00

link: https://people.umass.edu/jboke/wrotelearning/nice-gantt-charts-latex/
slug: nice-gantt-charts-latex
categories:
- latex
---


<style>
.hljs {
    background: #ffffff !important;
    border: 1px solid #e1e1e1;
}
</style>


The `pgfgantt` package in $\LaTeX$ provides amazing functionality for professional Gantt charts. It's my go to in writing proposals. 

See the code I used to create the Gantt chart shown below (it's a pretty busy chart!):

```latex
\documentclass{article}
\usepackage[margin=1in]{geometry}
\usepackage{pgfplots}
\usepackage{pgfgantt}
%... (truncated - full code below)
```

<details>
<summary>Click to view the full code</summary>

```latex
\documentclass{article}
\usepackage[margin=1in]{geometry}
\usepackage{pgfplots}
\usepackage{pgfgantt}
\usepackage{graphicx} % Required for inserting images
\pgfplotsset{compat=newest}
\makeatletter
\def\pgfcalendarmonthshortername#1{%
  \pgfutil@translate{\ifcase#1\or Ja\or Fe\or Ma\or Ap\or
    Ma\or Ju\or Ju\or Au\or Se\or Oc\or
    No\or De\fi}%
}
\def\pgfcalendarmonthsingleletter#1{%
  \tiny
  \pgfutil@translate{\ifcase#1\or J\or F\or M\or A\or
    M\or J\or J\or A\or S\or O\or
    N\or D\fi}%
}
\makeatother


\title{gantt-chart-example}
\author{Jimi Oke}
\date{January 2024}

\begin{document}

\pagestyle{empty}
%\maketitle

\ganttset{group/.append style={orange},
milestone/.append style={draw=none},
progress label node anchor/.append style={text=red}}

  \newganttchartelement{project}{
    project/.style={% inner sep=0pt,
      draw=none,
      fill=blue!60!black      
    },
    project label font ={\color{white}\bfseries\scriptsize\sffamily},
  }

  \newganttchartelement{admin}{
    admin/.style={% inner sep=0pt,
      draw=none,
      fill=red!80!black      
    },
    admin label font ={\color{white}\bfseries\scriptsize\sffamily},
  }


  \newganttchartelement{dci}{
    dci/.style={      
      draw=none,
      fill = orange
    },
    dci label font ={\color{white}\bfseries\scriptsize\sffamily},
    % raThreebar left shift=.1, raThreebar right shift=-.1
  }
  \newganttchartelement{pub}{
    pub/.style={      
      draw=none,
      fill = green!50!black
    },
    pub label font ={\color{white}\bfseries\scriptsize\sffamily},
    % raThreebar left shift=.1, raThreebar right shift=-.1
  }


  \begin{ganttchart}[y unit title=0.4cm,
    y unit chart=0.33cm,
    x unit=0.25cm,
    % hgrid,
   % hgrid style/.style={black, solid},
    vgrid, %={black, solid},
    %title/.style={draw=gray},
    title label anchor/.style={below=-1.6ex},
    %group label node/.append style={draw},
   % title left shift=.05,
   % title right shift=-.05,
    title height=1,
    title label font={\footnotesize\sffamily},
    group label font={\bfseries\footnotesize\sffamily},
    group/.append style={fill=gray},
    bar/.style={fill=green!50!black!50!},
    bar incomplete/.style={fill=red!40},
    bar label font={\scriptsize\sffamily},
    canvas/.append style={fill=none},
    progress label text={},
    milestone height = .6,
    bar top shift=0.1,
    bar height=.8,
    group right shift=0,
    group top shift=0.2,
    group height=.8,
    time slot format=isodate-yearmonth,
    time slot unit=month,
    link/.style={->},
    group inline label node/.style={yshift=0pt,font=\color{white}\bfseries\scriptsize\sffamily},
    milestone inline label node/.append style={right=0mm},
    milestone label node/.append style={font=\scriptsize\bfseries\sffamily},
    workshopR/.style={milestone/.append style={fill=blue!60!black,shape=isosceles triangle},
    milestone inline label node/.append style={right=1mm}},
    milestoneR/.style={milestone/.append style={fill=blue!60!black}},    
    milestoneL/.style={milestone/.append style={fill=blue!60!black},
    milestone inline label node/.append style={left=0mm,font=\bfseries\scriptsize\bfseries\sffamily}},        
    workshopL/.style={milestone/.append style={fill=blue!60!black,shape=isosceles triangle},milestone inline label node/.append style={left=0mm}},
    deliverableR/.style={milestone/.append style={fill=blue!60!black,shape=rectangle}},
    deliverableL/.style={milestone/.append style={fill=blue!60!black,shape=rectangle},
     milestone inline label node/.append style={left=0mm,font=\bfseries\scriptsize\sffamily}},
    deliverableT3L/.style={milestone/.append style={fill=orange,shape=rectangle},
     milestone inline label node/.append style={left=0mm,font=\bfseries\scriptsize\sffamily}},  
    deliverableT5L/.style={milestone/.append style={fill=green!50!black,shape=rectangle},
     milestone inline label node/.append style={left=0mm,font=\bfseries\scriptsize\sffamily}},       
    deliverableT3R/.style={milestone/.append style={fill=orange,shape=rectangle},
     milestone inline label node/.append style={right=0mm,font=\bfseries\scriptsize\sffamily}},
    webinarL/.style={milestone/.append style={fill=green!50!black,shape=isosceles triangle},
    milestone inline label node/.append style={left=0mm,font=\bfseries\scriptsize\bfseries\sffamily}},
    adminprsL/.style={milestone/.append style={fill=red!80!black,shape=rectangle},
    milestone inline label node/.append style={left=0mm,font=\bfseries\scriptsize\bfseries\sffamily}},    
    admincallsL/.style={milestone/.append style={fill=red!80!black,shape=isosceles triangle},
    milestone inline label node/.append style={left=0mm,font=\bfseries\scriptsize\bfseries\sffamily}},
    admincallsR/.style={milestone/.append style={fill=red!80!black,shape=isosceles triangle},
    milestone inline label node/.append style={right=1mm,font=\bfseries\scriptsize\bfseries\sffamily}},    
    admindelivR/.style={milestone/.append style={fill=red!80!black,shape=rectangle},
    milestone inline label node/.append style={right=0mm,font=\bfseries\scriptsize\bfseries\sffamily}},    
    scmeetingsL/.style={milestone/.append style={fill=red!80!black,shape=isosceles triangle},
    milestone inline label node/.append style={left=0mm,font=\bfseries\scriptsize\bfseries\sffamily}},
    scmeetingsR/.style={milestone/.append style={fill=red!80!black,shape=isosceles triangle},
    milestone inline label node/.append style={right=0mm,font=\bfseries\scriptsize\bfseries\sffamily}}        
    ]{2023-9}{2028-12}
    % labels
    % \gantttitle{'21}{1}
    % \gantttitlecalendar{year, month=singleletter}\\
    \gantttitle{2023}{4}
    \gantttitle{2024}{12}
    \gantttitle{2025}{12}
    \gantttitle{2026}{12}
    \gantttitle{2027}{12}
    \gantttitle{2028}{12}
    \\
    \gantttitle{}{1}    
    \gantttitle{Q4}{3}
    \gantttitle{Q1}{3}
    \gantttitle{Q2}{3}
    \gantttitle{Q3}{3}
    \gantttitle{Q4}{3}
    \gantttitle{Q1}{3}
    \gantttitle{Q2}{3}
    \gantttitle{Q3}{3}
    \gantttitle{Q4}{3}
    \gantttitle{Q1}{3}
    \gantttitle{Q2}{3}
    \gantttitle{Q3}{3}
    \gantttitle{Q4}{3}
    \gantttitle{Q1}{3}
    \gantttitle{Q2}{3}
    \gantttitle{Q3}{3}
    \gantttitle{Q4}{3}    
    \gantttitle{Q1}{3}
    \gantttitle{Q2}{3}
    \gantttitle{Q3}{3}
    \gantttitle{Q4}{3}    
    \\
    % tasks
    \ganttgroup[inline=true]{Task 1: Administration and reporting}{2023-10}{2028-12} \\ 
    %\ganttadmin[inline=true]{T1.3 Monthly conference calls}{2023-11}{2028-09}\\
    \ganttmilestone[adminprsL,inline=true]{D1.2}{2024-1}
    \ganttmilestone[adminprsL,inline=true]{}{2024-4}
    \ganttmilestone[adminprsL,inline=true]{}{2024-7}
    \ganttmilestone[adminprsL,inline=true]{}{2024-10}
    \ganttmilestone[adminprsL,inline=true]{}{2025-1}
    \ganttmilestone[adminprsL,inline=true]{}{2025-4}
    \ganttmilestone[adminprsL,inline=true]{}{2025-7}
    \ganttmilestone[adminprsL,inline=true]{}{2025-10}
    \ganttmilestone[adminprsL,inline=true]{}{2026-1}
    \ganttmilestone[adminprsL,inline=true]{}{2026-4}
    \ganttmilestone[adminprsL,inline=true]{}{2026-7}
    \ganttmilestone[adminprsL,inline=true]{}{2026-10}
    \ganttmilestone[adminprsL,inline=true]{}{2027-1}
    \ganttmilestone[adminprsL,inline=true]{}{2027-4}
    \ganttmilestone[adminprsL,inline=true]{}{2027-7}
    \ganttmilestone[adminprsL,inline=true]{}{2027-10}
    \ganttmilestone[adminprsL,inline=true]{}{2028-1}
    \ganttmilestone[adminprsL,inline=true]{}{2028-4}
    \ganttmilestone[adminprsL,inline=true]{}{2028-7}
    \ganttmilestone[adminprsL,inline=true]{}{2028-10}\\    
   % \ganttadmin[inline=true]{T1.3 Monthly conference calls}{2023-11}{2028-09}\\
    \ganttmilestone[admincallsR,inline=true]{M1.1 Kick-off meeting}{2023-10}\\    
    \ganttmilestone[admincallsL,inline=true]{M1.2}{2023-12}
    \ganttmilestone[admincallsL,inline=true]{}{2024-1}
    \ganttmilestone[admincallsL,inline=true]{}{2024-2}
    \ganttmilestone[admincallsL,inline=true]{}{2024-3}
    \ganttmilestone[admincallsL,inline=true]{}{2024-4}
    \ganttmilestone[admincallsL,inline=true]{}{2024-5}
    \ganttmilestone[admincallsL,inline=true]{}{2024-6}
    \ganttmilestone[admincallsL,inline=true]{}{2024-7}
    \ganttmilestone[admincallsL,inline=true]{}{2024-8}
    \ganttmilestone[admincallsL,inline=true]{}{2024-9}
    \ganttmilestone[admincallsL,inline=true]{}{2024-10}
    \ganttmilestone[admincallsL,inline=true]{}{2024-11}
    \ganttmilestone[admincallsL,inline=true]{}{2024-12}    
    \ganttmilestone[admincallsL,inline=true]{}{2025-1}
    \ganttmilestone[admincallsL,inline=true]{}{2025-2}
    \ganttmilestone[admincallsL,inline=true]{}{2025-3}
    \ganttmilestone[admincallsL,inline=true]{}{2025-4}
    \ganttmilestone[admincallsL,inline=true]{}{2025-5}
    \ganttmilestone[admincallsL,inline=true]{}{2025-6}
    \ganttmilestone[admincallsL,inline=true]{}{2025-7}
    \ganttmilestone[admincallsL,inline=true]{}{2025-8}
    \ganttmilestone[admincallsL,inline=true]{}{2025-9}
    \ganttmilestone[admincallsL,inline=true]{}{2025-10}
    \ganttmilestone[admincallsL,inline=true]{}{2025-11}
    \ganttmilestone[admincallsL,inline=true]{}{2025-12} 
    \ganttmilestone[admincallsL,inline=true]{}{2026-1}
    \ganttmilestone[admincallsL,inline=true]{}{2026-2}
    \ganttmilestone[admincallsL,inline=true]{}{2026-3}
    \ganttmilestone[admincallsL,inline=true]{}{2026-4}
    \ganttmilestone[admincallsL,inline=true]{}{2026-5}
    \ganttmilestone[admincallsL,inline=true]{}{2026-6}
    \ganttmilestone[admincallsL,inline=true]{}{2026-7}
    \ganttmilestone[admincallsL,inline=true]{}{2026-8}
    \ganttmilestone[admincallsL,inline=true]{}{2026-9}
    \ganttmilestone[admincallsL,inline=true]{}{2026-10}
    \ganttmilestone[admincallsL,inline=true]{}{2026-11}
    \ganttmilestone[admincallsL,inline=true]{}{2026-12}    
    \ganttmilestone[admincallsL,inline=true]{}{2027-1}
    \ganttmilestone[admincallsL,inline=true]{}{2027-2}
    \ganttmilestone[admincallsL,inline=true]{}{2027-3}
    \ganttmilestone[admincallsL,inline=true]{}{2027-4}
    \ganttmilestone[admincallsL,inline=true]{}{2027-5}
    \ganttmilestone[admincallsL,inline=true]{}{2027-6}
    \ganttmilestone[admincallsL,inline=true]{}{2027-7}
    \ganttmilestone[admincallsL,inline=true]{}{2027-8}
    \ganttmilestone[admincallsL,inline=true]{}{2027-9}
    \ganttmilestone[admincallsL,inline=true]{}{2027-10}
    \ganttmilestone[admincallsL,inline=true]{}{2027-11}
    \ganttmilestone[admincallsL,inline=true]{}{2027-12}
    \ganttmilestone[admincallsL,inline=true]{}{2028-1}
    \ganttmilestone[admincallsL,inline=true]{}{2028-2}
    \ganttmilestone[admincallsL,inline=true]{}{2028-3}
    \ganttmilestone[admincallsL,inline=true]{}{2028-4}
    \ganttmilestone[admincallsL,inline=true]{}{2028-5}
    \ganttmilestone[admincallsL,inline=true]{}{2028-6}
    \ganttmilestone[admincallsL,inline=true]{}{2028-7}
    \ganttmilestone[admincallsL,inline=true]{}{2028-8}
    \ganttmilestone[admincallsL,inline=true]{}{2028-9}\\  
    \ganttgroup[inline=true]{Task 2: Steering committee}{2023-10}{2028-4} \\ 
    %\ganttadmin[inline=true]{T2.1 Identify stakeholders}{2023-10}{2024-1}\\
    \ganttmilestone[admindelivR,inline=true]{D2.1 Steering committee members}{2024-2}\\ 
    \ganttmilestone[scmeetingsL,inline=true]{M2.1 Mtgs.}{2024-4}
    \ganttmilestone[scmeetingsL,inline=true]{}{2024-10}
    \ganttmilestone[scmeetingsL,inline=true]{}{2025-4}
    \ganttmilestone[scmeetingsL,inline=true]{}{2025-10}
    \ganttmilestone[scmeetingsL,inline=true]{}{2026-4}
    \ganttmilestone[scmeetingsL,inline=true]{}{2026-10}
    \ganttmilestone[scmeetingsL,inline=true]{}{2027-4}
    \ganttmilestone[scmeetingsL,inline=true]{}{2027-10}
    \ganttmilestone[scmeetingsL,inline=true]{}{2028-4}\\        
    \ganttgroup[inline=true]{Task 3: Define, Coordinate, Integrate}{2023-10}{2028-9} \\ 
    % \ganttdci[inline=true]{3.1 Preliminary literature review}{2023-09}{2023-10}\\
    % \ganttdci[inline=true]{3.2 Prepare research agenda}{2023-09}{2023-10}\\    
    % \ganttdci[inline=true]{3.3 Coordination}{2023-09}{2028-09}\\        
    \ganttmilestone[deliverableT3R, milestone label  font=\scriptsize\sffamily, inline=true]{D3.1: Performance metrics report \& preliminary review}{2023-11} \\
    \ganttmilestone[deliverableT3R, milestone label  font=\scriptsize\sffamily, inline=true]{D3.2: 5-year research agenda}{2023-11} \\
    \ganttmilestone[deliverableT3L, milestone label  font=\scriptsize\sffamily, inline=true]{D3.3 Agenda updates}{2024-9}
    \ganttmilestone[deliverableT3L, milestone label  font=\scriptsize\sffamily, inline=true]{}{2025-9}
    \ganttmilestone[deliverableT3L, milestone label  font=\scriptsize\sffamily, inline=true]{}{2026-9}
    \ganttmilestone[deliverableT3L, milestone label  font=\scriptsize\sffamily, inline=true]{}{2027-9}
    \ganttmilestone[deliverableT3L, milestone label  font=\scriptsize\sffamily, inline=true]{}{2028-9}    
    \\    
    
    
    \ganttgroup[inline=true]{Task 4: Conduct Research Projects}{2023-10}{2028-09} \\ %\myline{thin}{blue}
    
    \ganttproject[name = t11, inline=true]{T4.1: Dynamic research synthesis}{2023-10}{2027-06}\\
    \ganttmilestone[workshopR, milestone label  font=\bfseries\scriptsize\sffamily,inline=true]{W4.1.1 Research Needs workshop}{2024-3} \\
    \ganttmilestone[deliverableR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.1.1: Systematic literature review}{2024-9} \\
    \ganttmilestone[workshopR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{W4.1.2 Dynamic Synthesis workshop}{2025-9} \\      
    \ganttmilestone[milestoneR, milestone label font=\bfseries\scriptsize\bfseries\sffamily, inline=true]{M4.1.1 Prototype dynamic synthesis pipeline}{2026-9} \\        
    \ganttmilestone[deliverableR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.1.2 AI dynamic synthesis framework}{2026-12} \\    

        %%% T4.2
    \ganttproject[name = t42, inline]{T4.2: Establish infrastructure and protocols}{2024-02}{2027-09} \\
    \ganttmilestone[workshopR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{W4.2.1 Standards workshop}{2024-6} \\    
    \ganttmilestone[milestoneR, milestone label font=\bfseries\scriptsize\bfseries\sffamily, inline=true]{M4.1.1 Platform prototype V1.0}{2024-9} \\    
    \ganttmilestone[workshopR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{W4.2.2 Protocols workshop}{2025-6} \\     
    \ganttmilestone[milestoneR, milestone label font=\bfseries\scriptsize\bfseries\sffamily, inline=true]{M4.1.2 Platform prototype V2.0}{2025-12} \\           
    \ganttmilestone[deliverableR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.2.1 Standards/protocols guidance}{2026-3} \\
    \ganttmilestone[deliverableR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.2.2 Platform \& sharing infrastructure}{2026-12} \\    
 
    
    %%% T4.3
    \ganttproject[name = t43, inline]{T4.3: Define benchmarks and best practices}{2024-01}{2028-3} \\   
    \ganttmilestone[milestoneR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{M4.3.1 Candidate benchmark datasets/models}{2024-12} \\        
    \ganttmilestone[workshopR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{W4.3.1 Landmark Models workshop}{2025-3} \\  
    \ganttmilestone[milestoneR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{M4.3.2 Internal validation topics}{2025-12} \\      
    \ganttmilestone[workshopR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{W4.3.2 Internal Validation workshop}{2026-3} \\ 
    \ganttmilestone[milestoneR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{M4.3.3 Criteria for benchmark selection}{2026-6} \\          

    \ganttmilestone[deliverableR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.3.1 Benchmarks}{2026-9} \\    
     \ganttmilestone[deliverableR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.3.2 Internal validation guide}{2026-9} \\    
     \ganttmilestone[deliverableR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.3.3 Illustrative examples}{2026-12} \\    

    %%%% T4.4.
    \ganttproject[name = t44, inline]{T4.4: Identify performance metric “North Stars:”}{2024-1}{2027-09}\\
    \ganttmilestone[workshopR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{W4.4.1: North Stars I workshop}{2024-12} \\
    \ganttmilestone[milestoneR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{M4.4.1 North Star candidates and selection process}{2025-9} \\
    \ganttmilestone[workshopR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{W4.4.2: North Stars II workshop}{2026-12} \\                
    \ganttmilestone[deliverableL, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.4.1 Final list of North Stars and process}{2027-3} \\    
    \ganttmilestone[deliverableL, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.4.2 North Star program evaluation}{2027-6} \\    


     %% T4.5
    \ganttproject[name = t45, inline=true]{T4.5: Strengthen existing knowledge}{2024-03}{2028-03}\\  \ganttmilestone[workshopR, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{W4.5.1 Large-scale Simulation workshop}{2024-9} \\
    \ganttmilestone[milestoneR, milestone label font=\scriptsize\bfseries\sffamily, inline=true]{M4.5.1 Large-scale simulation framework: AVs}{2025-3} \\     
    \ganttmilestone[milestoneL, milestone label font=\scriptsize\bfseries\sffamily, inline=true]{M4.5.2 Large-scale simulation framework: shared mobility}{2026-6} \\     
    \ganttmilestone[workshopL, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{W4.5.2 Advances \& Experiments workshop}{2027-3} \\ 
    \ganttmilestone[deliverableL, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.5.1 On-demand taxi application}{2027-6} \\  
    \ganttmilestone[deliverableL, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.5.2 Shared bikes and e-bikes application}{2027-9} \\  
    \ganttmilestone[deliverableL, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.5.3 Shared AVs application}{2027-12} \\      
    
    \ganttproject[name = t45, inline]{T4.6: Discover high-interest scenarios}{2024-06}{2028-09}\\  
    \ganttmilestone[milestoneR, milestone label font=\scriptsize\bfseries\sffamily, inline=true]{M4.6.1 Scenario space}{2024-9} \\       
    \ganttmilestone[milestoneR, milestone label font=\scriptsize\bfseries\sffamily, inline=true]{M4.6.2 Candidate strategies}{2024-12} \\       
    \ganttmilestone[milestoneR, milestone label font=\scriptsize\bfseries\sffamily, inline=true]{M4.6.3 Preliminary meta-model methods }{2025-9} \\           
    \ganttmilestone[workshopL, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{W4.6.1: Experimental Design \& Meta-modeling workshop}{2026-6} \\
    \ganttmilestone[deliverableL, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.6.1: Scenario discovery framework}{2026-9} \\  
\ganttmilestone[milestoneL, milestone label font=\scriptsize\bfseries\sffamily, inline=true]        {M4.6.4 Preliminary SD data mining and analysis methods}{2027-1} \\               
    \ganttmilestone[workshopL, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{W4.6.2: Robust Policy Analyses workshop}{2027-11} \\   
    \ganttmilestone[deliverableL, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.6.2: High-interest scenarios}{2028-4} \\  
    \ganttmilestone[deliverableL, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D4.6.3: Robust NAM policy recommendations}{2028-7} \\   
    
    \ganttgroup[inline=true]{Task 5: Publish research and engage with stakeholders}{2023-10}{2028-12}\\    
    \ganttpub[name = t45, inline]{T5.2 Share and transfer knowledge via WISEN-UP Network Platform}{2024-01}{2028-12}\\ 
    \ganttpub[name = t45, inline]{T5.3 Plan/host workshops, webinars and conference sessions}{2024-01}{2028-9}\\       
    \ganttmilestone[name = web1, webinarL,inline=true]{W5.1 Webinars}{2024-07} %{2024-02} 
    \ganttmilestone[name = web1, webinarL,inline=true]{}{2025-07}
    \ganttmilestone[name = web1, webinarL,inline=true]{}{2026-07}
    \ganttmilestone[name = web1, webinarL,inline=true]{}{2027-07}
    \ganttmilestone[name = web1, webinarL,inline=true]{}{2028-07}\\
    \ganttmilestone[deliverableT5L,inline=true]{D5.1 White papers}{2024-09} %{2024-02} 
    \ganttmilestone[deliverableT5L,inline=true]{}{2025-09}
    \ganttmilestone[deliverableT5L,inline=true]{}{2026-09}
    \ganttmilestone[deliverableT5L,inline=true]{}{2027-09}
    \ganttmilestone[deliverableT5L,inline=true]{}{2028-09}    
    \\
    % \ganttmilestone[deliverableT5L, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D5.1}{2026-9} \\  
   \ganttmilestone[deliverableT5L, milestone label  font=\bfseries\scriptsize\sffamily, inline=true]{D5.2 Final Report}{2028-12} 
    
    % \ganttlink{elem3}{elem4}
    % \ganttlink{elem1}{elem5}
    % \ganttlink{elem3}{elem5}
    % \ganttlink{elem2}{elem6}
    % \ganttlink{elem3}{elem6}
    % \ganttlink{elem5}{elem7}    
    % \begin{scope}[minimum height=0mm, minimum width= 2mm,node distance=.75mm]
    % \node[fill=red!80!black, draw=none] (qprhandle) at ([yshift=-25pt]current bounding box.south){};
    % \node[minimum width=2mm,isosceles triangle, isosceles triangle stretches, fill=red!80!black, draw=none, below=of qprhandle] (scmhandle) {};
    % %   \node[fill=cyan, draw, below=of raTwohandle] (raThreehandle) {};
    % \end{scope}
    % \begin{scope}[node distance=.75mm, font={\scriptsize\sffamily}]
    %    \node[right= of qprhandle] {Quarterly progress reports};
    %    \node[right= of scmhandle] {Steering Committee meetings};
    % %   \node[right= of raTwohandle] {Research Assistant 2 (1 year)};
    % %   \node[right= of raThreehandle] {Research Assistant 3 (3 years)};
    % \end{scope}
  \end{ganttchart}
\end{document}
```

</details>

{{< embed-pdf url="/files/gantt-chart-example-2.pdf" renderPageNum="1"  >}}

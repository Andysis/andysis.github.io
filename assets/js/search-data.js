// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-publications",
          title: "publications",
          description: "\# means co-first author, and \* means corresponding author.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-cv",
          title: "cv",
          description: "This is a description of the page. You can modify it in &#39;_pages/cv.md&#39;. You can also change or remove the top pdf download button.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "post-a-post-with-image-galleries",
      
        title: "a post with image galleries",
      
      description: "this is what included image galleries could look like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2024/photo-gallery/";
        
      },
    },{id: "post-google-gemini-updates-flash-1-5-gemma-2-and-project-astra",
      
        title: 'Google Gemini updates: Flash 1.5, Gemma 2 and Project Astra <svg width="1.2rem" height="1.2rem" top=".5rem" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><path d="M17 13.5v6H5v-12h6m3-3h6v6m0-6-9 9" class="icon_svg-stroke" stroke="#999" stroke-width="1.5" fill="none" fill-rule="evenodd" stroke-linecap="round" stroke-linejoin="round"></path></svg>',
      
      description: "We’re sharing updates across our Gemini family of models and a glimpse of Project Astra, our vision for the future of AI assistants.",
      section: "Posts",
      handler: () => {
        
          window.open("https://blog.google/technology/ai/google-gemini-update-flash-ai-assistant-io-2024/", "_blank");
        
      },
    },{id: "post-a-post-with-tabs",
      
        title: "a post with tabs",
      
      description: "this is what included tabs in a post could look like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2024/tabs/";
        
      },
    },{id: "post-a-post-with-typograms",
      
        title: "a post with typograms",
      
      description: "this is what included typograms code could look like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2024/typograms/";
        
      },
    },{id: "post-a-post-that-can-be-cited",
      
        title: "a post that can be cited",
      
      description: "this is what a post that can be cited looks like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2024/post-citation/";
        
      },
    },{id: "post-a-post-with-pseudo-code",
      
        title: "a post with pseudo code",
      
      description: "this is what included pseudo code could look like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2024/pseudocode/";
        
      },
    },{id: "post-a-post-with-code-diff",
      
        title: "a post with code diff",
      
      description: "this is how you can display code diffs",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2024/code-diff/";
        
      },
    },{id: "post-a-post-with-advanced-image-components",
      
        title: "a post with advanced image components",
      
      description: "this is what advanced image components could look like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2024/advanced-images/";
        
      },
    },{id: "post-a-post-with-vega-lite",
      
        title: "a post with vega lite",
      
      description: "this is what included vega lite code could look like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2024/vega-lite/";
        
      },
    },{id: "post-a-post-with-geojson",
      
        title: "a post with geojson",
      
      description: "this is what included geojson code could look like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2024/geojson-map/";
        
      },
    },{id: "post-a-post-with-echarts",
      
        title: "a post with echarts",
      
      description: "this is what included echarts code could look like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2024/echarts/";
        
      },
    },{id: "post-a-post-with-chart-js",
      
        title: "a post with chart.js",
      
      description: "this is what included chart.js code could look like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2024/chartjs/";
        
      },
    },{id: "post-a-post-with-tikzjax",
      
        title: "a post with TikZJax",
      
      description: "this is what included TikZ code could look like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2023/tikzjax/";
        
      },
    },{id: "post-a-post-with-bibliography",
      
        title: "a post with bibliography",
      
      description: "an example of a blog post with bibliography",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2023/post-bibliography/";
        
      },
    },{id: "post-a-post-with-jupyter-notebook",
      
        title: "a post with jupyter notebook",
      
      description: "an example of a blog post with jupyter notebook",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2023/jupyter-notebook/";
        
      },
    },{id: "post-a-post-with-custom-blockquotes",
      
        title: "a post with custom blockquotes",
      
      description: "an example of a blog post with custom blockquotes",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2023/custom-blockquotes/";
        
      },
    },{id: "post-a-post-with-table-of-contents-on-a-sidebar",
      
        title: "a post with table of contents on a sidebar",
      
      description: "an example of a blog post with table of contents on a sidebar",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2023/sidebar-table-of-contents/";
        
      },
    },{id: "post-a-post-with-audios",
      
        title: "a post with audios",
      
      description: "this is what included audios could look like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2023/audios/";
        
      },
    },{id: "post-a-post-with-videos",
      
        title: "a post with videos",
      
      description: "this is what included videos could look like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2023/videos/";
        
      },
    },{id: "post-displaying-beautiful-tables-with-bootstrap-tables",
      
        title: "displaying beautiful tables with Bootstrap Tables",
      
      description: "an example of how to use Bootstrap Tables",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2023/tables/";
        
      },
    },{id: "post-a-post-with-table-of-contents",
      
        title: "a post with table of contents",
      
      description: "an example of a blog post with table of contents",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2023/table-of-contents/";
        
      },
    },{id: "post-a-post-with-giscus-comments",
      
        title: "a post with giscus comments",
      
      description: "an example of a blog post with giscus comments",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2022/giscus-comments/";
        
      },
    },{id: "post-displaying-external-posts-on-your-al-folio-blog",
      
        title: 'Displaying External Posts on Your al-folio Blog <svg width="1.2rem" height="1.2rem" top=".5rem" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><path d="M17 13.5v6H5v-12h6m3-3h6v6m0-6-9 9" class="icon_svg-stroke" stroke="#999" stroke-width="1.5" fill="none" fill-rule="evenodd" stroke-linecap="round" stroke-linejoin="round"></path></svg>',
      
      description: "",
      section: "Posts",
      handler: () => {
        
          window.open("https://medium.com/@al-folio/displaying-external-posts-on-your-al-folio-blog-b60a1d241a0a?source=rss-17feae71c3c4------2", "_blank");
        
      },
    },{id: "post-a-post-with-redirect",
      
        title: "a post with redirect",
      
      description: "you can also redirect to assets like pdf",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/assets/pdf/example_pdf.pdf";
        
      },
    },{id: "post-a-post-with-diagrams",
      
        title: "a post with diagrams",
      
      description: "an example of a blog post with diagrams",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2021/diagrams/";
        
      },
    },{id: "post-a-distill-style-blog-post",
      
        title: "a distill-style blog post",
      
      description: "an example of a distill-style blog post and main elements",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2021/distill/";
        
      },
    },{id: "post-a-post-with-twitter",
      
        title: "a post with twitter",
      
      description: "an example of a blog post with twitter",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2020/twitter/";
        
      },
    },{id: "post-a-post-with-disqus-comments",
      
        title: "a post with disqus comments",
      
      description: "an example of a blog post with disqus comments",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2015/disqus-comments/";
        
      },
    },{id: "post-a-post-with-math",
      
        title: "a post with math",
      
      description: "an example of a blog post with some math",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2015/math/";
        
      },
    },{id: "post-a-post-with-code",
      
        title: "a post with code",
      
      description: "an example of a blog post with some code",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2015/code/";
        
      },
    },{id: "post-a-post-with-images",
      
        title: "a post with images",
      
      description: "this is what included images could look like",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2015/images/";
        
      },
    },{id: "post-a-post-with-formatting-and-links",
      
        title: "a post with formatting and links",
      
      description: "march &amp; april, looking forward to summer",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2015/formatting-and-links/";
        
      },
    },{id: "news-my-previous-email-address-zhiweiwang-hust-edu-cn-has-been-suspended-please-contact-me-via-the-new-one",
          title: 'My previous email address (zhiweiwang@hust.edu.cn) has been suspended! Please contact me via the...',
          description: "",
          section: "News",},{id: "news-a-first-authored-tmi-paper-has-been-accepted-congratulations",
          title: 'A first authored TMI paper has been accepted. Congratulations!',
          description: "",
          section: "News",},{id: "news-a-co-authored-miccai-paper-has-been-accepted-congratulations-to-xixi-jiang-and-prof-yang-s-team",
          title: 'A co-authored MICCAI paper has been accepted. Congratulations to Xixi Jiang and Prof....',
          description: "",
          section: "News",},{id: "news-my-previous-email-address-eezhiweiwang-ust-hk-has-been-suspended-please-contact-me-via-the-new-one",
          title: 'My previous email address (eezhiweiwang@ust.hk) has been suspended! Please contact me via the...',
          description: "",
          section: "News",},{id: "news-a-co-first-authored-miccai-paper-has-been-accepted-congratulations-to-junlin-xian-and-prof-yang",
          title: 'A co-first authored MICCAI paper has been accepted. Congratulations to Junlin Xian and...',
          description: "",
          section: "News",},{id: "news-a-co-frist-authored-acm-mm-paper-has-been-accepted-congratulations-to-hongkuan-shi",
          title: 'A co-frist authored ACM MM paper has been accepted. Congratulations to Hongkuan Shi!...',
          description: "",
          section: "News",},{id: "news-a-co-first-authored-fundamental-research-paper-about-vertebral-landmark-localization-has-been-accepted",
          title: 'A co-first authored Fundamental Research paper about Vertebral Landmark Localization has been accepted....',
          description: "",
          section: "News",},{id: "news-a-cooresponding-authored-miccai-challenge-paper-has-been-accepted-congratulations-to-sheng-wang-and-jinxin-lv",
          title: 'A cooresponding authored MICCAI Challenge paper has been accepted. Congratulations to Sheng Wang...',
          description: "",
          section: "News",},{id: "news-a-co-first-authored-tmi-paper-has-been-accepted-congratulations-to-jinxin-lv",
          title: 'A co-first authored TMI paper has been accepted. Congratulations to Jinxin Lv!',
          description: "",
          section: "News",},{id: "news-the-team-led-by-me-wins-the-national-second-price-in-全国大学生生命科学竞赛",
          title: 'The team led by me wins the National second price in 全国大学生生命科学竞赛.',
          description: "",
          section: "News",},{id: "news-i-am-awarded-ieee-tmi-bronze-distinguished-reviewer-for-the-years-2020-2022",
          title: 'I am awarded IEEE TMI Bronze Distinguished Reviewer for the years 2020-2022.',
          description: "",
          section: "News",},{id: "news-a-corresponding-authored-accv-paper-regarding-the-sparse-view-cbct-reconstruction-has-been-accepted-congratulations-to-yanli-wang-and-lianying-chao",
          title: 'A corresponding authored ACCV paper regarding the sparse-view CBCT reconstruction has been accepted....',
          description: "",
          section: "News",},{id: "news-a-corresponding-authored-aaai-paper-regarding-one-shot-brain-mri-segmentation-has-been-accepted-congratulations-to-jinxin-lv-and-xiaoyu-zeng-special-thanks-to-the-graduated-student-sheng-wang",
          title: 'A corresponding authored AAAI paper regarding one-shot brain MRI segmentation has been accepted....',
          description: "",
          section: "News",},{id: "news-a-corresponding-authored-jbhi-paper-regarding-cobb-angle-estimation-has-been-accepted-congratulations-to-yuanhuai-liang-and-jinxin-lv",
          title: 'A corresponding authored JBHI paper regarding Cobb angle estimation has been accepted. Congratulations...',
          description: "",
          section: "News",},{id: "news-a-first-authored-ijcai-paper-regarding-breast-cancer-diagnosis-has-been-accepted-congratulations",
          title: 'A first authored IJCAI paper regarding breast cancer diagnosis has been accepted. Congratulations!...',
          description: "",
          section: "News",},{id: "news-i-am-awarded-武汉英才-优青-for-the-year-2023",
          title: 'I am awarded 武汉英才（优青） for the year 2023.',
          description: "",
          section: "News",},{id: "news-a-co-first-authored-tmi-paper-regarding-stereo-depth-estimation-has-been-accepted-congratulations-to-hongkuan-shi",
          title: 'A co-first authored TMI paper regarding stereo depth estimation has been accepted. Congratulations...',
          description: "",
          section: "News",},{id: "news-the-team-led-by-me-wins-the-provincial-second-price-in-中国机器人及人工智能大赛",
          title: 'The team led by me wins the Provincial second price in 中国机器人及人工智能大赛.',
          description: "",
          section: "News",},{id: "news-the-team-led-by-me-wins-the-national-third-price-in-全国大学生生命科学竞赛",
          title: 'The team led by me wins the National third price in 全国大学生生命科学竞赛.',
          description: "",
          section: "News",},{id: "news-the-team-led-by-me-wins-the-national-first-price-in-中国机器人及人工智能大赛",
          title: 'The team led by me wins the National first price in 中国机器人及人工智能大赛.',
          description: "",
          section: "News",},{id: "news-two-corresponding-authored-bibm-papers-have-been-accepted-congratulations-to-lianying-chao-and-wenqi-shan",
          title: 'Two corresponding authored BIBM papers have been accepted. Congratulations to Lianying Chao and...',
          description: "",
          section: "News",},{id: "news-a-corresponding-authored-tmi-paper-has-been-accepted-congratulations-to-quan-zhou",
          title: 'A corresponding authored TMI paper has been accepted. Congratulations to Quan Zhou!',
          description: "",
          section: "News",},{id: "news-i-received-湖北省科技进步二等奖-in-2023",
          title: 'I received 湖北省科技进步二等奖 in 2023.',
          description: "",
          section: "News",},{id: "news-two-corresponding-authored-miccai-papers-have-been-accepted-congratulations-to-qiang-hu-and-chongwei-wu",
          title: 'Two corresponding authored MICCAI papers have been accepted. Congratulations to Qiang Hu and...',
          description: "",
          section: "News",},{id: "news-one-corresponding-authored-bibm-paper-has-been-accepted-congratulations-to-kaixiang-yang",
          title: 'One corresponding authored BIBM paper has been accepted. Congratulations to Kaixiang Yang!',
          description: "",
          section: "News",},{id: "news-one-corresponding-authored-bibm-paper-has-been-accepted-congratulations-to-ying-zhou",
          title: 'One corresponding authored BIBM paper has been accepted. Congratulations to Ying Zhou!',
          description: "",
          section: "News",},{id: "news-one-corresponding-authored-jbhi-paper-has-been-accepted-congratulations-to-fang-peng-hongkuan-shi-and-shiquan-he",
          title: 'One corresponding authored JBHI paper has been accepted. Congratulations to Fang Peng, Hongkuan...',
          description: "",
          section: "News",},{id: "news-one-corresponding-authored-aaai-paper-has-been-accepted-congratulations-to-qiang-hu",
          title: 'One corresponding authored AAAI paper has been accepted. Congratulations to Qiang Hu!',
          description: "",
          section: "News",},{id: "news-three-corresponding-authored-icassp-papers-are-accepted-congratulations-to-wenqi-shan-qiang-hu-and-kaixiang-yang",
          title: 'Three corresponding authored ICASSP papers are accepted. Congratulations to Wenqi Shan, Qiang Hu,...',
          description: "",
          section: "News",},{id: "news-one-first-authored-media-paper-is-accepted",
          title: 'One first authored MedIA paper is accepted!',
          description: "",
          section: "News",},{id: "news-one-corresponding-authored-jbhi-paper-is-accepted-congratulations-to-quan-zhou",
          title: 'One corresponding authored JBHI paper is accepted. Congratulations to Quan Zhou!',
          description: "",
          section: "News",},{id: "projects-project-1",
          title: 'project 1',
          description: "with background image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/1_project/";
            },},{id: "projects-project-2",
          title: 'project 2',
          description: "a project with a background image and giscus comments",
          section: "Projects",handler: () => {
              window.location.href = "/projects/2_project/";
            },},{id: "projects-project-3-with-very-long-name",
          title: 'project 3 with very long name',
          description: "a project that redirects to another website",
          section: "Projects",handler: () => {
              window.location.href = "/projects/3_project/";
            },},{id: "projects-project-4",
          title: 'project 4',
          description: "another without an image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/4_project/";
            },},{id: "projects-project-5",
          title: 'project 5',
          description: "a project with a background image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/5_project/";
            },},{id: "projects-project-6",
          title: 'project 6',
          description: "a project with no image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/6_project/";
            },},{id: "projects-project-7",
          title: 'project 7',
          description: "with background image",
          section: "Projects",handler: () => {
              window.location.href = "/projects/7_project/";
            },},{id: "projects-project-8",
          title: 'project 8',
          description: "an other project with a background image and giscus comments",
          section: "Projects",handler: () => {
              window.location.href = "/projects/8_project/";
            },},{id: "projects-project-9",
          title: 'project 9',
          description: "another project with an image 🎉",
          section: "Projects",handler: () => {
              window.location.href = "/projects/9_project/";
            },},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%7A%77%77%61%6E%67@%68%75%73%74.%65%64%75.%63%6E", "_blank");
        },
      },{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/Andysis", "_blank");
        },
      },{
        id: 'social-inspire',
        title: 'Inspire HEP',
        section: 'Socials',
        handler: () => {
          window.open("https://inspirehep.net/authors/1010907", "_blank");
        },
      },{
        id: 'social-orcid',
        title: 'ORCID',
        section: 'Socials',
        handler: () => {
          window.open("https://orcid.org/0000-0002-1612-8573", "_blank");
        },
      },{
        id: 'social-rss',
        title: 'RSS Feed',
        section: 'Socials',
        handler: () => {
          window.open("/feed.xml", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=Andy Wang", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];

export interface NewsArticle {
  id: string;
  title: string;
  summary: string;
  timestamp: string;
  source: string;
}

export interface Planet {
  id: string;
  name: string;
  color: string;
  size: number;
  articles: NewsArticle[];
}

export interface SolarSystem {
  id: string;
  name: string;
  color: string;
  planets: Planet[];
}

export interface Galaxy {
  id: string;
  name: string;
  color: string;
  gradient: string[];
  solarSystems: SolarSystem[];
}

export const newsData: Galaxy[] = [
  {
    id: 'politics',
    name: 'Politics & Governance',
    color: '#4F46E5',
    gradient: ['#4F46E5', '#7C3AED'],
    solarSystems: [
      {
        id: 'elections',
        name: 'Elections & Campaigns',
        color: '#6366F1',
        planets: [
          {
            id: 'national-elections',
            name: 'National Elections',
            color: '#818CF8',
            size: 40,
            articles: [
              {
                id: '1',
                title: 'Brazil Presidential Runoff Enters Final Week',
                summary: 'Final polls show tight race as candidates make last appeals to undecided voters in São Paulo and Rio.',
                timestamp: '2 hours ago',
                source: 'Global News Wire'
              },
              {
                id: '2',
                title: 'Colombia Midterm Results Shift Senate Balance',
                summary: 'Opposition parties gain ground in legislative elections, setting stage for policy debates.',
                timestamp: '5 hours ago',
                source: 'Latin America Daily'
              }
            ]
          },
          {
            id: 'digital-campaigns',
            name: 'Digital Campaign Ethics',
            color: '#A5B4FC',
            size: 30,
            articles: [
              {
                id: '3',
                title: 'New AI-Generated Campaign Ads Spark Controversy',
                summary: 'Ethics boards investigate deepfake videos used in political messaging.',
                timestamp: '1 hour ago',
                source: 'Tech Policy Review'
              }
            ]
          }
        ]
      },
      {
        id: 'geopolitics',
        name: 'Geopolitics & International Affairs',
        color: '#8B5CF6',
        planets: [
          {
            id: 'nato-disputes',
            name: 'Global Alliances',
            color: '#A78BFA',
            size: 45,
            articles: [
              {
                id: '4',
                title: 'NATO Summit Addresses Strategic Asset Sharing',
                summary: 'Member nations debate cybersecurity infrastructure and joint defense protocols.',
                timestamp: '3 hours ago',
                source: 'International Affairs Quarterly'
              }
            ]
          },
          {
            id: 'space-rights',
            name: 'Lunar Exploration Rights',
            color: '#C4B5FD',
            size: 35,
            articles: [
              {
                id: '5',
                title: 'UN Committee Debates Moon Resource Allocation',
                summary: 'Competing claims over lunar mining zones reach international tribunal.',
                timestamp: '6 hours ago',
                source: 'Space Policy Institute'
              }
            ]
          }
        ]
      },
      {
        id: 'public-policy',
        name: 'Public Policy',
        color: '#7C3AED',
        planets: [
          {
            id: 'medicaid',
            name: 'Medicaid Reform',
            color: '#9333EA',
            size: 32,
            articles: [
              {
                id: '6',
                title: 'Five States Expand Coverage Under New Federal Guidelines',
                summary: 'Healthcare access broadens as states adopt modified eligibility standards.',
                timestamp: '4 hours ago',
                source: 'Health Policy Watch'
              }
            ]
          }
        ]
      }
    ]
  },
  {
    id: 'technology',
    name: 'Science & Technology',
    color: '#06B6D4',
    gradient: ['#06B6D4', '#0EA5E9'],
    solarSystems: [
      {
        id: 'ai',
        name: 'Artificial Intelligence',
        color: '#22D3EE',
        planets: [
          {
            id: 'agentic-ai',
            name: 'Agentic AI',
            color: '#67E8F9',
            size: 50,
            articles: [
              {
                id: '7',
                title: 'Autonomous AI Agents Handle 40% of Customer Service',
                summary: 'Major retailers report AI systems independently resolving complex customer issues.',
                timestamp: '1 hour ago',
                source: 'AI Today'
              },
              {
                id: '8',
                title: 'OpenAI Unveils GPT-5 with Enhanced Reasoning',
                summary: 'New model demonstrates unprecedented multi-step problem solving capabilities.',
                timestamp: '30 minutes ago',
                source: 'Tech Frontier'
              }
            ]
          },
          {
            id: 'ai-bias',
            name: 'Algorithmic Bias',
            color: '#A5F3FC',
            size: 38,
            articles: [
              {
                id: '9',
                title: 'Study Reveals Hiring AI Discriminates Against Career Gaps',
                summary: 'Research shows recruitment algorithms penalize resume gaps disproportionately.',
                timestamp: '2 hours ago',
                source: 'Ethics in Tech Journal'
              }
            ]
          },
          {
            id: 'ai-slop',
            name: 'AI Misinformation',
            color: '#CFFAFE',
            size: 28,
            articles: [
              {
                id: '10',
                title: 'Social Platforms Combat AI-Generated "Slop" Content',
                summary: 'New detection systems identify low-quality synthetic media flooding feeds.',
                timestamp: '3 hours ago',
                source: 'Digital Media Watch'
              }
            ]
          }
        ]
      },
      {
        id: 'cybersecurity',
        name: 'Cybersecurity',
        color: '#0EA5E9',
        planets: [
          {
            id: 'state-hacking',
            name: 'State-Linked Hacking',
            color: '#38BDF8',
            size: 42,
            articles: [
              {
                id: '11',
                title: 'Energy Grid Attack Traced to Foreign Actors',
                summary: 'Cybersecurity firms identify coordinated intrusion attempts on power infrastructure.',
                timestamp: '1 hour ago',
                source: 'Cyber Defense Weekly'
              }
            ]
          },
          {
            id: 'deepfake-verification',
            name: 'Deepfake Verification',
            color: '#7DD3FC',
            size: 36,
            articles: [
              {
                id: '12',
                title: 'New Blockchain-Based Video Authentication Launched',
                summary: 'Startup offers real-time verification to combat synthetic media manipulation.',
                timestamp: '4 hours ago',
                source: 'Security Innovation'
              }
            ]
          }
        ]
      },
      {
        id: 'space-tech',
        name: 'Space & Frontier Tech',
        color: '#0284C7',
        planets: [
          {
            id: 'lunar-missions',
            name: 'Commercial Lunar Missions',
            color: '#0369A1',
            size: 40,
            articles: [
              {
                id: '13',
                title: 'SpaceX Starship Lands First Cargo on Moon',
                summary: 'Historic mission delivers construction equipment for permanent lunar base.',
                timestamp: '8 hours ago',
                source: 'Space Exploration News'
              }
            ]
          }
        ]
      }
    ]
  },
  {
    id: 'health',
    name: 'Health & Society',
    color: '#10B981',
    gradient: ['#10B981', '#14B8A6'],
    solarSystems: [
      {
        id: 'public-health',
        name: 'Public Health',
        color: '#34D399',
        planets: [
          {
            id: 'mental-health',
            name: 'Mental Health',
            color: '#6EE7B7',
            size: 44,
            articles: [
              {
                id: '14',
                title: 'Youth Anxiety Rates Drop for First Time Since 2019',
                summary: 'New study credits digital wellness programs and improved school support systems.',
                timestamp: '2 hours ago',
                source: 'Public Health Journal'
              }
            ]
          },
          {
            id: 'nutrition',
            name: 'Nutrition Assistance',
            color: '#A7F3D0',
            size: 35,
            articles: [
              {
                id: '15',
                title: 'SNAP Benefits Expand to Cover Fresh Produce Delivery',
                summary: 'Federal program now includes direct-to-consumer farm partnerships.',
                timestamp: '5 hours ago',
                source: 'Health America'
              }
            ]
          }
        ]
      },
      {
        id: 'education',
        name: 'Education',
        color: '#14B8A6',
        planets: [
          {
            id: 'misinformation-literacy',
            name: 'Misinformation Literacy',
            color: '#5EEAD4',
            size: 38,
            articles: [
              {
                id: '16',
                title: 'New Curriculum Teaches Students to Spot AI-Generated Fakes',
                summary: 'Schools nationwide adopt critical thinking framework for digital age.',
                timestamp: '3 hours ago',
                source: 'Education Weekly'
              }
            ]
          }
        ]
      }
    ]
  },
  {
    id: 'business',
    name: 'Business & Economy',
    color: '#F59E0B',
    gradient: ['#F59E0B', '#EF4444'],
    solarSystems: [
      {
        id: 'geoeconomics',
        name: 'Geoeconomics',
        color: '#FBBF24',
        planets: [
          {
            id: 'rare-earth',
            name: 'Rare Earth Minerals',
            color: '#FCD34D',
            size: 46,
            articles: [
              {
                id: '17',
                title: 'New Lithium Deposits Discovered in Nevada',
                summary: 'Find could reduce US dependency on foreign battery material imports.',
                timestamp: '4 hours ago',
                source: 'Economic Times'
              }
            ]
          },
          {
            id: 'supply-chain',
            name: 'Supply Chain Resilience',
            color: '#FDE68A',
            size: 40,
            articles: [
              {
                id: '18',
                title: 'Manufacturers Adopt "Just-in-Case" Inventory Strategies',
                summary: 'Companies stockpile critical components amid global uncertainty.',
                timestamp: '6 hours ago',
                source: 'Business Insider'
              }
            ]
          }
        ]
      },
      {
        id: 'ai-infrastructure',
        name: 'AI Infrastructure',
        color: '#F97316',
        planets: [
          {
            id: 'data-centers',
            name: 'Data Center Energy',
            color: '#FB923C',
            size: 42,
            articles: [
              {
                id: '19',
                title: 'Tech Giants Invest $50B in Nuclear-Powered Data Centers',
                summary: 'Microsoft, Google, Amazon partner with nuclear startups for clean AI energy.',
                timestamp: '2 hours ago',
                source: 'Tech Finance'
              }
            ]
          }
        ]
      }
    ]
  },
  {
    id: 'environment',
    name: 'Environment & Climate',
    color: '#22C55E',
    gradient: ['#22C55E', '#84CC16'],
    solarSystems: [
      {
        id: 'climate-impact',
        name: 'Climate Impact',
        color: '#4ADE80',
        planets: [
          {
            id: 'climate-migration',
            name: 'Climate Migration',
            color: '#86EFAC',
            size: 40,
            articles: [
              {
                id: '20',
                title: 'Pacific Island Nations Plan Mass Relocation',
                summary: 'Rising sea levels force governments to negotiate resettlement agreements.',
                timestamp: '5 hours ago',
                source: 'Climate Watch'
              }
            ]
          }
        ]
      },
      {
        id: 'sustainability',
        name: 'Sustainability & Energy',
        color: '#84CC16',
        planets: [
          {
            id: 'renewable-energy',
            name: 'Renewable Energy',
            color: '#BEF264',
            size: 48,
            articles: [
              {
                id: '21',
                title: 'Solar Power Surpasses Coal in Global Energy Mix',
                summary: 'Renewables reach historic milestone as costs continue to decline.',
                timestamp: '1 hour ago',
                source: 'Green Energy Report'
              }
            ]
          }
        ]
      }
    ]
  },
  {
    id: 'culture',
    name: 'Lifestyle & Culture',
    color: '#EC4899',
    gradient: ['#EC4899', '#A855F7'],
    solarSystems: [
      {
        id: 'entertainment',
        name: 'Entertainment',
        color: '#F472B6',
        planets: [
          {
            id: 'movie-releases',
            name: 'Movie Reviews',
            color: '#F9A8D4',
            size: 38,
            articles: [
              {
                id: '22',
                title: 'Sci-Fi Epic "Starborne" Breaks Opening Weekend Records',
                summary: 'Immersive theater experience draws massive crowds worldwide.',
                timestamp: '3 hours ago',
                source: 'Entertainment Weekly'
              }
            ]
          }
        ]
      },
      {
        id: 'sports',
        name: 'Sports',
        color: '#A855F7',
        planets: [
          {
            id: 'olympics',
            name: '2026 Winter Olympics',
            color: '#C084FC',
            size: 44,
            articles: [
              {
                id: '23',
                title: 'USA Takes Gold in Team Figure Skating',
                summary: 'Historic performance caps off dominant showing in Milan-Cortina games.',
                timestamp: '2 hours ago',
                source: 'Sports Daily'
              }
            ]
          }
        ]
      }
    ]
  }
];

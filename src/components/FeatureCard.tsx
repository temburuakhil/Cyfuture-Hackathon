import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent } from '@/components/ui/card';

interface FeatureCardProps {
  title: string;
  description: string;
  icon: any; // LucideIcon
  link: string;
  benefits?: string[];
  color?: string;
  gradient?: string;
}

const FeatureCard: React.FC<FeatureCardProps> = ({ 
  title, 
  description, 
  icon: Icon,
  link,
  benefits,
  color = 'bg-blue-500',
  gradient = 'from-blue-500 to-blue-600'
}) => {
  const navigate = useNavigate();

  return (
    <Card 
      className="cursor-pointer hover:shadow-lg transition-shadow"
      onClick={() => navigate(link)}
    >
      <CardContent className="p-6">
        <div className="flex items-start space-x-4">
          <div className={`p-2 rounded-lg text-white ${color}`}>
            <Icon className="h-6 w-6" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-lg">{title}</h3>
            <p className="text-sm text-muted-foreground">{description}</p>
            {benefits && benefits.length > 0 && (
              <ul className="mt-3 space-y-1">
                {benefits.map((benefit, index) => (
                  <li key={index} className="text-sm text-muted-foreground flex items-center">
                    <span className={`w-1.5 h-1.5 rounded-full ${color} mr-2`} />
                    {benefit}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default FeatureCard;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Heart, Users, MapPin, Utensils, Camera, Sparkles, Music, Palette, Mail, Car, Flower2, CheckCircle2, IndianRupee, TrendingUp, Gift, Calendar } from 'lucide-react';
import './App.css';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [step, setStep] = useState('budget');
  const [guestCount, setGuestCount] = useState(200);
  const [totalBudget, setTotalBudget] = useState(1000000); // 10 lakhs default
  const [selectedVenue, setSelectedVenue] = useState(null);
  const [selectedCuisines, setSelectedCuisines] = useState([]);
  const [selectedServices, setSelectedServices] = useState([]);
  
  const [venues, setVenues] = useState([]);
  const [cuisines, setCuisines] = useState([]);
  const [services, setServices] = useState({});
  const [calculatedBudget, setCalculatedBudget] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    if (selectedVenue || selectedCuisines.length > 0 || selectedServices.length > 0) {
      calculateBudget();
    }
  }, [selectedVenue, selectedCuisines, selectedServices, guestCount]);

  const fetchData = async () => {
    try {
      const [venuesRes, cuisinesRes, servicesRes] = await Promise.all([
        axios.get(`${API_URL}/api/venues`),
        axios.get(`${API_URL}/api/cuisine-options`),
        axios.get(`${API_URL}/api/services`)
      ]);
      setVenues(venuesRes.data.venues);
      setCuisines(cuisinesRes.data.cuisines);
      setServices(servicesRes.data.services);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const calculateBudget = async () => {
    try {
      const response = await axios.post(`${API_URL}/api/calculate-budget`, {
        guest_count: guestCount,
        venue_id: selectedVenue?.id,
        cuisine_ids: selectedCuisines.map(c => c.id),
        service_ids: selectedServices.map(s => s.id)
      });
      setCalculatedBudget(response.data);
    } catch (error) {
      console.error('Error calculating budget:', error);
    }
  };

  const formatCurrency = (amount) => {
    if (amount >= 100000) {
      return `₹${(amount / 100000).toFixed(1)}L`;
    }
    return `₹${amount.toLocaleString('en-IN')}`;
  };

  const getUsedBudget = () => {
    return calculatedBudget?.total_cost || 0;
  };

  const getRemainingBudget = () => {
    return totalBudget - getUsedBudget();
  };

  const getBudgetPercentage = () => {
    return (getUsedBudget() / totalBudget) * 100;
  };

  const toggleCuisine = (cuisine) => {
    if (selectedCuisines.find(c => c.id === cuisine.id)) {
      setSelectedCuisines(selectedCuisines.filter(c => c.id !== cuisine.id));
    } else {
      setSelectedCuisines([...selectedCuisines, cuisine]);
    }
  };

  const toggleService = (service) => {
    if (selectedServices.find(s => s.id === service.id)) {
      setSelectedServices(selectedServices.filter(s => s.id !== service.id));
    } else {
      setSelectedServices([...selectedServices, service]);
    }
  };

  const categoryIcons = {
    'Photography': Camera,
    'Decorations': Palette,
    'Entertainment': Music,
    'Makeup': Sparkles,
    'Invitations': Mail,
    'Transportation': Car,
    'Mehendi': Flower2
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blush via-ivory to-champagne">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-md sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Heart className="w-8 h-8 text-rose-gold fill-rose-gold" />
              <h1 className="text-3xl font-bold text-rose-gold">Budget Wedding Planner</h1>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600">Your Dream Wedding</p>
              <p className="text-lg font-semibold text-rose-gold">₹5L - ₹20L Range</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Budget Overview Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 border-2 border-rose-gold/20">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Left: Budget Circle */}
            <div className="flex flex-col items-center justify-center">
              <div className="relative w-64 h-64">
                <svg className="w-full h-full transform -rotate-90">
                  <circle
                    cx="128"
                    cy="128"
                    r="110"
                    stroke="#FFE5E5"
                    strokeWidth="20"
                    fill="none"
                  />
                  <circle
                    cx="128"
                    cy="128"
                    r="110"
                    stroke="#B76E79"
                    strokeWidth="20"
                    fill="none"
                    strokeDasharray={`${2 * Math.PI * 110}`}
                    strokeDashoffset={`${2 * Math.PI * 110 * (1 - getBudgetPercentage() / 100)}`}
                    strokeLinecap="round"
                    className="transition-all duration-500"
                  />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <p className="text-4xl font-bold text-rose-gold">{getBudgetPercentage().toFixed(0)}%</p>
                  <p className="text-gray-600 text-sm mt-1">Budget Used</p>
                </div>
              </div>
              <div className="mt-6 text-center">
                <p className="text-2xl font-bold text-gray-800">{formatCurrency(getUsedBudget())}</p>
                <p className="text-gray-600">of {formatCurrency(totalBudget)}</p>
              </div>
            </div>

            {/* Right: Budget Settings */}
            <div className="space-y-6">
              <div>
                <label className="flex items-center text-lg font-semibold text-gray-700 mb-3">
                  <IndianRupee className="w-5 h-5 mr-2 text-rose-gold" />
                  Total Budget
                </label>
                <input
                  type="range"
                  min="500000"
                  max="2000000"
                  step="50000"
                  value={totalBudget}
                  onChange={(e) => setTotalBudget(Number(e.target.value))}
                  className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                />
                <div className="flex justify-between mt-2">
                  <span className="text-sm text-gray-600">₹5L</span>
                  <span className="text-xl font-bold text-rose-gold">{formatCurrency(totalBudget)}</span>
                  <span className="text-sm text-gray-600">₹20L</span>
                </div>
              </div>

              <div>
                <label className="flex items-center text-lg font-semibold text-gray-700 mb-3">
                  <Users className="w-5 h-5 mr-2 text-rose-gold" />
                  Guest Count
                </label>
                <input
                  type="range"
                  min="50"
                  max="1000"
                  step="10"
                  value={guestCount}
                  onChange={(e) => setGuestCount(Number(e.target.value))}
                  className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                />
                <div className="flex justify-between mt-2">
                  <span className="text-sm text-gray-600">50</span>
                  <span className="text-xl font-bold text-rose-gold">{guestCount} guests</span>
                  <span className="text-sm text-gray-600">1000</span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mt-6 pt-6 border-t">
                <div className="bg-green-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600">Remaining</p>
                  <p className="text-xl font-bold text-green-600">{formatCurrency(getRemainingBudget())}</p>
                </div>
                <div className="bg-rose-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600">Spent</p>
                  <p className="text-xl font-bold text-rose-600">{formatCurrency(getUsedBudget())}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-2xl shadow-lg p-2 mb-8 flex space-x-2 overflow-x-auto">
          {[
            { id: 'budget', label: 'Budget', icon: IndianRupee },
            { id: 'venue', label: 'Venue', icon: MapPin },
            { id: 'cuisine', label: 'Cuisine', icon: Utensils },
            { id: 'services', label: 'Services', icon: Gift },
            { id: 'summary', label: 'Summary', icon: TrendingUp }
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setStep(tab.id)}
                className={`flex-1 flex items-center justify-center space-x-2 px-6 py-3 rounded-xl font-semibold transition-all ${
                  step === tab.id
                    ? 'bg-rose-gold text-white shadow-lg'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="whitespace-nowrap">{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Venue Selection */}
        {step === 'venue' && (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-4xl font-bold text-gray-800 mb-2">Choose Your Perfect Venue</h2>
              <p className="text-gray-600">Select a beautiful location for your special day</p>
            </div>
            <div className="grid md:grid-cols-2 gap-6">
              {venues.map((venue) => (
                <div
                  key={venue.id}
                  onClick={() => setSelectedVenue(venue)}
                  className={`bg-white rounded-2xl shadow-lg overflow-hidden cursor-pointer transform transition-all hover:scale-105 ${
                    selectedVenue?.id === venue.id ? 'ring-4 ring-rose-gold' : ''
                  }`}
                >
                  <div className="relative h-48 overflow-hidden">
                    <img src={venue.image} alt={venue.name} className="w-full h-full object-cover" />
                    {selectedVenue?.id === venue.id && (
                      <div className="absolute top-4 right-4 bg-rose-gold text-white p-2 rounded-full">
                        <CheckCircle2 className="w-6 h-6" />
                      </div>
                    )}
                  </div>
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="text-2xl font-bold text-gray-800">{venue.name}</h3>
                      <span className="bg-rose-gold text-white px-3 py-1 rounded-full text-sm font-semibold">
                        {formatCurrency(venue.price)}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-3">{venue.description}</p>
                    <div className="flex items-center text-sm text-gray-500 mb-3">
                      <Users className="w-4 h-4 mr-1" />
                      <span>{venue.capacity}</span>
                      <span className="mx-2">•</span>
                      <span className="font-semibold">{venue.price_range}</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {venue.amenities.map((amenity, idx) => (
                        <span key={idx} className="bg-blush text-rose-gold px-3 py-1 rounded-full text-xs font-medium">
                          {amenity}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Cuisine Selection */}
        {step === 'cuisine' && (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-4xl font-bold text-gray-800 mb-2">Select Your Menu</h2>
              <p className="text-gray-600">Delight your guests with delicious cuisine (you can select multiple)</p>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {cuisines.map((cuisine) => {
                const isSelected = selectedCuisines.find(c => c.id === cuisine.id);
                return (
                  <div
                    key={cuisine.id}
                    onClick={() => toggleCuisine(cuisine)}
                    className={`bg-white rounded-2xl shadow-lg p-6 cursor-pointer transform transition-all hover:scale-105 ${
                      isSelected ? 'ring-4 ring-rose-gold' : ''
                    }`}
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div className="bg-rose-gold/10 p-3 rounded-full">
                        <Utensils className="w-8 h-8 text-rose-gold" />
                      </div>
                      {isSelected && (
                        <div className="bg-rose-gold text-white p-2 rounded-full">
                          <CheckCircle2 className="w-5 h-5" />
                        </div>
                      )}
                    </div>
                    <h3 className="text-xl font-bold text-gray-800 mb-2">{cuisine.name}</h3>
                    <p className="text-gray-600 text-sm mb-3">{cuisine.description}</p>
                    <div className="bg-blush p-3 rounded-lg mb-3">
                      <p className="text-rose-gold font-bold text-lg">₹{cuisine.price_per_plate}/plate</p>
                      <p className="text-gray-600 text-xs">For {guestCount} guests: {formatCurrency(cuisine.price_per_plate * guestCount)}</p>
                    </div>
                    <div className="space-y-1">
                      <p className="text-xs font-semibold text-gray-700">Popular Dishes:</p>
                      {cuisine.popular_dishes.slice(0, 3).map((dish, idx) => (
                        <p key={idx} className="text-xs text-gray-600">• {dish}</p>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Services Selection */}
        {step === 'services' && (
          <div className="space-y-8">
            <div className="text-center mb-8">
              <h2 className="text-4xl font-bold text-gray-800 mb-2">Essential Wedding Services</h2>
              <p className="text-gray-600">Choose services to make your wedding memorable</p>
            </div>
            {Object.keys(services).map((category) => {
              const Icon = categoryIcons[category] || Gift;
              return (
                <div key={category}>
                  <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
                    <Icon className="w-6 h-6 mr-3 text-rose-gold" />
                    {category}
                  </h3>
                  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {services[category].map((service) => {
                      const isSelected = selectedServices.find(s => s.id === service.id);
                      return (
                        <div
                          key={service.id}
                          onClick={() => toggleService(service)}
                          className={`bg-white rounded-xl shadow-md p-5 cursor-pointer transition-all hover:shadow-lg ${
                            isSelected ? 'ring-2 ring-rose-gold bg-rose-50' : ''
                          }`}
                        >
                          <div className="flex justify-between items-start mb-3">
                            <h4 className="font-bold text-gray-800 flex-1">{service.name}</h4>
                            {isSelected && (
                              <CheckCircle2 className="w-5 h-5 text-rose-gold flex-shrink-0 ml-2" />
                            )}
                          </div>
                          <p className="text-sm text-gray-600 mb-3">{service.description}</p>
                          <div className="flex justify-between items-center">
                            <span className="text-lg font-bold text-rose-gold">{formatCurrency(service.price)}</span>
                            <span className="text-xs bg-gray-100 px-2 py-1 rounded-full">{service.package_type}</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Summary */}
        {step === 'summary' && (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-4xl font-bold text-gray-800 mb-2">Your Wedding Plan Summary</h2>
              <p className="text-gray-600">Review your selections and budget breakdown</p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {/* Left: Selections */}
              <div className="space-y-4">
                {/* Venue */}
                {selectedVenue && (
                  <div className="bg-white rounded-xl shadow-lg p-6">
                    <h3 className="text-xl font-bold text-rose-gold mb-4 flex items-center">
                      <MapPin className="w-5 h-5 mr-2" />
                      Venue
                    </h3>
                    <div className="flex items-center space-x-4">
                      <img src={selectedVenue.image} alt={selectedVenue.name} className="w-20 h-20 rounded-lg object-cover" />
                      <div className="flex-1">
                        <p className="font-bold text-gray-800">{selectedVenue.name}</p>
                        <p className="text-sm text-gray-600">{selectedVenue.capacity}</p>
                      </div>
                      <p className="font-bold text-rose-gold">{formatCurrency(selectedVenue.price)}</p>
                    </div>
                  </div>
                )}

                {/* Cuisine */}
                {selectedCuisines.length > 0 && (
                  <div className="bg-white rounded-xl shadow-lg p-6">
                    <h3 className="text-xl font-bold text-rose-gold mb-4 flex items-center">
                      <Utensils className="w-5 h-5 mr-2" />
                      Cuisine ({guestCount} guests)
                    </h3>
                    <div className="space-y-3">
                      {selectedCuisines.map((cuisine) => (
                        <div key={cuisine.id} className="flex justify-between items-center">
                          <div>
                            <p className="font-semibold text-gray-800">{cuisine.name}</p>
                            <p className="text-sm text-gray-600">₹{cuisine.price_per_plate}/plate</p>
                          </div>
                          <p className="font-bold text-rose-gold">{formatCurrency(cuisine.price_per_plate * guestCount)}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Services */}
                {selectedServices.length > 0 && (
                  <div className="bg-white rounded-xl shadow-lg p-6">
                    <h3 className="text-xl font-bold text-rose-gold mb-4 flex items-center">
                      <Gift className="w-5 h-5 mr-2" />
                      Services
                    </h3>
                    <div className="space-y-2">
                      {selectedServices.map((service) => {
                        const Icon = categoryIcons[service.category] || Gift;
                        return (
                          <div key={service.id} className="flex justify-between items-center py-2 border-b last:border-b-0">
                            <div className="flex items-center space-x-2">
                              <Icon className="w-4 h-4 text-rose-gold" />
                              <span className="text-gray-800">{service.name}</span>
                            </div>
                            <p className="font-semibold text-rose-gold">{formatCurrency(service.price)}</p>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>

              {/* Right: Budget Breakdown */}
              <div className="space-y-4">
                <div className="bg-gradient-to-br from-rose-gold to-rose-600 text-white rounded-xl shadow-lg p-6">
                  <h3 className="text-2xl font-bold mb-6">Budget Breakdown</h3>
                  {calculatedBudget && calculatedBudget.breakdown.map((item, idx) => (
                    <div key={idx} className="flex justify-between items-center py-3 border-b border-white/20 last:border-b-0">
                      <div>
                        <p className="font-semibold">{item.item}</p>
                        <p className="text-xs opacity-80">{item.category}</p>
                        {item.details && <p className="text-xs opacity-70">{item.details}</p>}
                      </div>
                      <p className="font-bold text-lg">{formatCurrency(item.cost)}</p>
                    </div>
                  ))}
                  <div className="mt-6 pt-6 border-t-2 border-white/30">
                    <div className="flex justify-between items-center mb-2">
                      <p className="text-xl font-bold">Total Cost:</p>
                      <p className="text-3xl font-bold">{formatCurrency(getUsedBudget())}</p>
                    </div>
                    <div className="flex justify-between items-center">
                      <p className="opacity-90">Remaining Budget:</p>
                      <p className="text-xl font-bold">{formatCurrency(getRemainingBudget())}</p>
                    </div>
                  </div>
                </div>

                {/* Checklist */}
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <h3 className="text-xl font-bold text-rose-gold mb-4 flex items-center">
                    <Calendar className="w-5 h-5 mr-2" />
                    Wedding Planning Checklist
                  </h3>
                  <div className="space-y-2">
                    {[
                      'Book venue and confirm date',
                      'Finalize catering menu',
                      'Book photography/videography',
                      'Order wedding invitations',
                      'Book makeup artist',
                      'Arrange decorations',
                      'Book entertainment/DJ',
                      'Finalize guest list',
                      'Plan wedding attire',
                      'Arrange transportation'
                    ].map((task, idx) => (
                      <div key={idx} className="flex items-center space-x-3 p-2 hover:bg-gray-50 rounded">
                        <input type="checkbox" className="w-5 h-5 text-rose-gold rounded" />
                        <span className="text-gray-700">{task}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {step === 'budget' && (
          <div className="text-center py-12">
            <Heart className="w-24 h-24 text-rose-gold mx-auto mb-6 animate-pulse" />
            <h2 className="text-4xl font-bold text-gray-800 mb-4">Welcome to Your Wedding Planner!</h2>
            <p className="text-xl text-gray-600 mb-8">Set your budget and guest count above, then start planning your dream wedding</p>
            <button
              onClick={() => setStep('venue')}
              className="bg-rose-gold text-white px-8 py-4 rounded-full font-bold text-lg shadow-lg hover:bg-rose-600 transform transition-all hover:scale-105"
            >
              Start Planning →
            </button>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white/80 backdrop-blur-md mt-12 py-6">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-600">
            💝 Budget Wedding Planner - Making your dream wedding affordable
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Perfect for middle-class families with budgets between ₹5-20 lakhs
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;

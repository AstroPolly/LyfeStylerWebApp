import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, X, Clock, Calendar, Bell, Type, Palette, Repeat, Tag, Plus, User, LogOut, Mail, Lock, Eye, EyeOff, UserPlus, Settings, Home } from 'lucide-react';

interface Tag {
  id: number;
  name: string;
  color: string;
}

interface EventData {
  title: string;
  startTime: string;
  endTime: string;
  isRange: boolean;
  isRecurring: boolean;
  recurrenceDays: number;
  reminder: boolean;
  reminderMinutes: number;
  color: string;
  description: string;
  tags: number[];
}

interface RegisterData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

interface LoginData {
  email: string;
  password: string;
}

interface User {
  email: string;
  name: string;
}

const ScheduleApp = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState<'home' | 'register' | 'login' | 'account'>('home');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User>({ email: '', name: '' });
  const [showPassword, setShowPassword] = useState(false);
  
  // State for event form
  const [eventData, setEventData] = useState<EventData>({
    title: '',
    startTime: '09:00',
    endTime: '10:00',
    isRange: true,
    isRecurring: false,
    recurrenceDays: 7,
    reminder: false,
    reminderMinutes: 15,
    color: '#3B82F6',
    description: '',
    tags: []
  });

  // State for registration
  const [registerData, setRegisterData] = useState<RegisterData>({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  // State for login
  const [loginData, setLoginData] = useState<LoginData>({
    email: '',
    password: ''
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  // Available tags (could be loaded from storage in real app)
  const [availableTags, setAvailableTags] = useState<Tag[]>([
    { id: 1, name: 'Учеба', color: '#3B82F6' },
    { id: 2, name: 'Работа', color: '#10B981' },
    { id: 3, name: 'Встреча', color: '#8B5CF6' },
    { id: 4, name: 'Личное', color: '#F59E0B' }
  ]);
  
  const [newTagName, setNewTagName] = useState('');
  const [newTagColor, setNewTagColor] = useState('#3B82F6');

  const today = new Date();

  // Получение дней месяца
  const getDaysInMonth = (year: number, month: number): number => {
    return new Date(year, month + 1, 0).getDate();
  };

  // Получение первого дня месяца (0 = воскресенье, 1 = понедельник, и т.д.)
  const getFirstDayOfMonth = (year: number, month: number): number => {
    return new Date(year, month, 1).getDay();
  };

  // Названия месяцев
  const monthNames = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ];

  // Названия дней недели
  const weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];

  useEffect(() => {
    // Check if user is authenticated (in real app, check localStorage or session)
    const savedUser = localStorage.getItem('scheduleUser');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
      setIsAuthenticated(true);
    }
  }, []);

  // Переключение месяца назад
  const prevMonth = () => {
    setCurrentDate(prev => {
      const newDate = new Date(prev);
      newDate.setMonth(newDate.getMonth() - 1);
      return newDate;
    });
  };

  // Переключение месяца вперед
  const nextMonth = () => {
    setCurrentDate(prev => {
      const newDate = new Date(prev);
      newDate.setMonth(newDate.getMonth() + 1);
      return newDate;
    });
  };

  // Переключение года назад
  const prevYear = () => {
    setCurrentDate(prev => {
      const newDate = new Date(prev);
      newDate.setFullYear(newDate.getFullYear() - 1);
      return newDate;
    });
  };

  // Переключение года вперед
  const nextYear = () => {
    setCurrentDate(prev => {
      const newDate = new Date(prev);
      newDate.setFullYear(newDate.getFullYear() + 1);
      return newDate;
    });
  };

  // Генерация дней для отображения
  const renderCalendarDays = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const daysInMonth = getDaysInMonth(year, month);
    const firstDay = getFirstDayOfMonth(year, month);
    
    const days = [];
    
    // Добавляем пустые ячейки для дней предыдущего месяца
    for (let i = 0; i < firstDay; i++) {
      if (i === 0) i = 7; // Корректировка для понедельника как первого дня
      days.push(<div key={`empty-${i}`} className="h-12"></div>);
    }
    
    // Добавляем дни текущего месяца
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(year, month, day);
      const isToday = 
        date.getDate() === today.getDate() &&
        date.getMonth() === today.getMonth() &&
        date.getFullYear() === today.getFullYear();
      
      const isSelected = 
        date.getDate() === selectedDate.getDate() &&
        date.getMonth() === selectedDate.getMonth() &&
        date.getFullYear() === selectedDate.getFullYear();
      
      days.push(
        <button
          key={day}
          onClick={() => setSelectedDate(date)}
          className={`h-12 w-12 rounded-lg flex items-center justify-center text-sm font-medium transition-all duration-200 hover:bg-gray-100 ${
            isToday 
              ? 'ring-2 ring-blue-500 ring-offset-2 bg-blue-50 text-blue-700 font-semibold' 
              : isSelected
              ? 'bg-blue-100 text-blue-800 font-semibold'
              : 'text-gray-700 hover:text-gray-900'
          }`}
        >
          {day}
        </button>
      );
    }
    
    return days;
  };

  const handleInputChange = (field: keyof EventData, value: any) => {
    setEventData(prev => ({ ...prev, [field]: value }));
  };

  const toggleTag = (tagId: number) => {
    setEventData(prev => {
      const tags = [...prev.tags];
      const index = tags.indexOf(tagId);
      if (index > -1) {
        tags.splice(index, 1);
      } else {
        tags.push(tagId);
      }
      return { ...prev, tags };
    });
  };

  const addNewTag = () => {
    if (newTagName.trim()) {
      const newTag = {
        id: Date.now(),
        name: newTagName.trim(),
        color: newTagColor
      };
      setAvailableTags(prev => [...prev, newTag]);
      setNewTagName('');
      // Auto-select the new tag
      setEventData(prev => ({ ...prev, tags: [...prev.tags, newTag.id] }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Event created:', { ...eventData, date: selectedDate });
    setIsModalOpen(false);
    // Reset form
    setEventData({
      title: '',
      startTime: '09:00',
      endTime: '10:00',
      isRange: true,
      isRecurring: false,
      recurrenceDays: 7,
      reminder: false,
      reminderMinutes: 15,
      color: '#3B82F6',
      description: '',
      tags: []
    });
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    // Basic validation
    if (registerData.password !== registerData.confirmPassword) {
      setError('Пароли не совпадают');
      setLoading(false);
      return;
    }
    
    try {
      // This would be an API call to your backend in a real app
      // For demo purposes, we'll simulate a successful registration
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Save user data (in real app, this would come from the backend after successful registration)
      const newUser = {
        name: registerData.name,
        email: registerData.email
      };
      
      setUser(newUser);
      setIsAuthenticated(true);
      localStorage.setItem('scheduleUser', JSON.stringify(newUser));
      
      // Reset form and go to home page
      setRegisterData({ name: '', email: '', password: '', confirmPassword: '' });
      setCurrentPage('home');
    } catch (err) {
      setError('Ошибка при регистрации. Попробуйте еще раз.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      // This would be an API call to your backend in a real app
      // For demo purposes, we'll simulate a successful login
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // In a real app, you would get user data from the backend
      const mockUser = {
        name: loginData.email.split('@')[0],
        email: loginData.email
      };
      
      setUser(mockUser);
      setIsAuthenticated(true);
      localStorage.setItem('scheduleUser', JSON.stringify(mockUser));
      
      // Reset form and go to home page
      setLoginData({ email: '', password: '' });
      setCurrentPage('home');
    } catch (err) {
      setError('Неверный email или пароль');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    // Clear user data
    setUser({ email: '', name: '' });
    setIsAuthenticated(false);
    localStorage.removeItem('scheduleUser');
    setCurrentPage('home');
  };

  const handleRegisterChange = (field: keyof RegisterData, value: string) => {
    setRegisterData(prev => ({ ...prev, [field]: value }));
  };

  const handleLoginChange = (field: keyof LoginData, value: string) => {
    setLoginData(prev => ({ ...prev, [field]: value }));
  };

  const colorOptions = [
    { name: 'Синий', value: '#3B82F6' },
    { name: 'Зеленый', value: '#10B981' },
    { name: 'Фиолетовый', value: '#8B5CF6' },
    { name: 'Оранжевый', value: '#F59E0B' },
    { name: 'Красный', value: '#EF4444' },
    { name: 'Розовый', value: '#EC4899' }
  ];

  // Render different pages
  const renderPageContent = () => {
    if (currentPage === 'register') {
      return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-8">
            <div className="text-center mb-8">
              <div className="flex items-center justify-center mb-4">
                <Calendar className="w-10 h-10 text-blue-500" />
                <span className="ml-2 text-2xl font-bold text-gray-800">Расписание</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-800">Создать аккаунт</h2>
              <p className="text-gray-600 mt-2">Зарегистрируйтесь для доступа ко всем функциям</p>
            </div>
            
            {error && (
              <div className="mb-4 p-3 bg-red-50 text-red-500 rounded-lg text-sm">
                {error}
              </div>
            )}
            
            <form onSubmit={handleRegister} className="space-y-4">
              <div>
                <label className="flex items-center text-sm font-medium text-gray-700 mb-1">
                  <User className="w-4 h-4 mr-2 text-gray-500" />
                  Имя
                </label>
                <input
                  type="text"
                  value={registerData.name}
                  onChange={(e) => handleRegisterChange('name', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Ваше имя"
                  required
                />
              </div>
              
              <div>
                <label className="flex items-center text-sm font-medium text-gray-700 mb-1">
                  <Mail className="w-4 h-4 mr-2 text-gray-500" />
                  Email
                </label>
                <input
                  type="email"
                  value={registerData.email}
                  onChange={(e) => handleRegisterChange('email', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="example@email.com"
                  required
                />
              </div>
              
              <div>
                <label className="flex items-center text-sm font-medium text-gray-700 mb-1">
                  <Lock className="w-4 h-4 mr-2 text-gray-500" />
                  Пароль
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    value={registerData.password}
                    onChange={(e) => handleRegisterChange('password', e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Минимум 6 символов"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-2.5 text-gray-500 hover:text-gray-700"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
              
              <div>
                <label className="flex items-center text-sm font-medium text-gray-700 mb-1">
                  <Lock className="w-4 h-4 mr-2 text-gray-500" />
                  Подтвердите пароль
                </label>
                <input
                  type="password"
                  value={registerData.confirmPassword}
                  onChange={(e) => handleRegisterChange('confirmPassword', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Повторите пароль"
                  required
                />
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-500 text-white py-3 rounded-lg font-medium hover:bg-blue-600 transition-colors focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Регистрация...' : 'Зарегистрироваться'}
              </button>
            </form>
            
            <div className="mt-6 text-center">
              <p className="text-gray-600">Уже есть аккаунт?</p>
              <button
                onClick={() => setCurrentPage('login')}
                className="mt-2 text-blue-500 hover:text-blue-600 font-medium transition-colors"
              >
                Войти в систему
              </button>
            </div>
          </div>
        </div>
      );
    }
    
    if (currentPage === 'login') {
      return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-8">
            <div className="text-center mb-8">
              <div className="flex items-center justify-center mb-4">
                <Calendar className="w-10 h-10 text-blue-500" />
                <span className="ml-2 text-2xl font-bold text-gray-800">Расписание</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-800">Вход в аккаунт</h2>
              <p className="text-gray-600 mt-2">Введите свои данные для входа</p>
            </div>
            
            {error && (
              <div className="mb-4 p-3 bg-red-50 text-red-500 rounded-lg text-sm">
                {error}
              </div>
            )}
            
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="flex items-center text-sm font-medium text-gray-700 mb-1">
                  <Mail className="w-4 h-4 mr-2 text-gray-500" />
                  Email
                </label>
                <input
                  type="email"
                  value={loginData.email}
                  onChange={(e) => handleLoginChange('email', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="example@email.com"
                  required
                />
              </div>
              
              <div>
                <label className="flex items-center text-sm font-medium text-gray-700 mb-1">
                  <Lock className="w-4 h-4 mr-2 text-gray-500" />
                  Пароль
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    value={loginData.password}
                    onChange={(e) => handleLoginChange('password', e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Ваш пароль"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-2.5 text-gray-500 hover:text-gray-700"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    id="remember"
                    type="checkbox"
                    className="rounded text-blue-600 focus:ring-blue-500"
                  />
                  <label htmlFor="remember" className="ml-2 text-sm text-gray-600">
                    Запомнить меня
                  </label>
                </div>
                <a href="#" className="text-sm text-blue-500 hover:text-blue-600">
                  Забыли пароль?
                </a>
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-500 text-white py-3 rounded-lg font-medium hover:bg-blue-600 transition-colors focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Вход...' : 'Войти'}
              </button>
            </form>
            
            <div className="mt-6 text-center">
              <p className="text-gray-600">Нет аккаунта?</p>
              <button
                onClick={() => setCurrentPage('register')}
                className="mt-2 text-blue-500 hover:text-blue-600 font-medium transition-colors"
              >
                Зарегистрироваться
              </button>
            </div>
          </div>
        </div>
      );
    }
    
    if (currentPage === 'account') {
      return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center">
                  <div className="bg-blue-500 text-white w-12 h-12 rounded-full flex items-center justify-center">
                    <User className="w-6 h-6" />
                  </div>
                  <div className="ml-4">
                    <h1 className="text-2xl font-bold text-gray-800">{user.name}</h1>
                    <p className="text-gray-600">{user.email}</p>
                  </div>
                </div>
                <button
                  onClick={handleLogout}
                  className="flex items-center px-4 py-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <LogOut className="w-4 h-4 mr-2" />
                  Выйти
                </button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h2 className="text-xl font-semibold text-gray-800 mb-4">Информация об аккаунте</h2>
                  <div className="space-y-4">
                    <div className="flex items-center p-4 bg-gray-50 rounded-lg">
                      <Mail className="w-5 h-5 text-gray-500 mr-3" />
                      <div>
                        <p className="text-sm text-gray-500">Email</p>
                        <p className="font-medium">{user.email}</p>
                      </div>
                    </div>
                    <div className="flex items-center p-4 bg-gray-50 rounded-lg">
                      <Calendar className="w-5 h-5 text-gray-500 mr-3" />
                      <div>
                        <p className="text-sm text-gray-500">Дата регистрации</p>
                        <p className="font-medium">15 ноября 2023</p>
                      </div>
                    </div>
                    <div className="flex items-center p-4 bg-gray-50 rounded-lg">
                      <Settings className="w-5 h-5 text-gray-500 mr-3" />
                      <div>
                        <p className="text-sm text-gray-500">Статус аккаунта</p>
                        <p className="font-medium text-green-600">Активен</p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h2 className="text-xl font-semibold text-gray-800 mb-4">Настройки</h2>
                  <div className="space-y-4">
                    <button className="w-full flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                      <div>
                        <p className="font-medium text-gray-800">Изменить пароль</p>
                        <p className="text-sm text-gray-500">Обновите свой пароль для безопасности</p>
                      </div>
                      <ChevronRight className="w-5 h-5 text-gray-400" />
                    </button>
                    
                    <button className="w-full flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                      <div>
                        <p className="font-medium text-gray-800">Уведомления</p>
                        <p className="text-sm text-gray-500">Настройте, как и когда получать уведомления</p>
                      </div>
                      <ChevronRight className="w-5 h-5 text-gray-400" />
                    </button>
                    
                    <button className="w-full flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                      <div>
                        <p className="font-medium text-gray-800">Приватность</p>
                        <p className="text-sm text-gray-500">Управляйте своими данными и приватностью</p>
                      </div>
                      <ChevronRight className="w-5 h-5 text-gray-400" />
                    </button>
                    
                    <button className="w-full flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                      <div>
                        <p className="font-medium text-gray-800">Синхронизация</p>
                        <p className="text-sm text-gray-500">Настройте синхронизацию с другими устройствами</p>
                      </div>
                      <ChevronRight className="w-5 h-5 text-gray-400" />
                    </button>
                  </div>
                </div>
              </div>
              
              <div className="mt-8 pt-8 border-t">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">Теги</h2>
                <div className="flex flex-wrap gap-2">
                  {availableTags.map((tag) => (
                    <span
                      key={tag.id}
                      className="px-3 py-1 rounded-full text-sm font-medium"
                      style={{ 
                        backgroundColor: tag.color,
                        color: '#ffffff'
                      }}
                    >
                      {tag.name}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      );
    }
    
    // Default home page (schedule)
    return (
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Расписание</h1>
          <p className="text-gray-600">Управляйте своим временем эффективно</p>
        </header>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Calendar Sidebar */}
          <div className="flex-1 max-w-md">
            <div className="bg-white rounded-2xl shadow-xl p-6">
              {/* Calendar Header */}
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                  <button
                    onClick={prevYear}
                    className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    aria-label="Предыдущий год"
                  >
                    <ChevronLeft className="w-4 h-4" />
                  </button>
                  <button
                    onClick={prevMonth}
                    className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    aria-label="Предыдущий месяц"
                  >
                    <ChevronLeft className="w-5 h-5" />
                  </button>
                </div>
                
                <div className="text-center">
                  <h2 className="text-xl font-semibold text-gray-800">
                    {monthNames[currentDate.getMonth()]}
                  </h2>
                  <p className="text-gray-600 text-sm">
                    {currentDate.getFullYear()}
                  </p>
                </div>
                
                <div className="flex items-center gap-2">
                  <button
                    onClick={nextMonth}
                    className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    aria-label="Следующий месяц"
                  >
                    <ChevronRight className="w-5 h-5" />
                  </button>
                  <button
                    onClick={nextYear}
                    className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    aria-label="Следующий год"
                  >
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Weekdays Header */}
              <div className="grid grid-cols-7 gap-2 mb-4">
                {weekdays.map((day) => (
                  <div
                    key={day}
                    className="h-8 flex items-center justify-center text-sm font-medium text-gray-500"
                  >
                    {day}
                  </div>
                ))}
              </div>

              {/* Calendar Days */}
              <div className="grid grid-cols-7 gap-2">
                {renderCalendarDays()}
              </div>

              {/* Selected Date Info */}
              <div className="mt-6 p-4 bg-blue-50 rounded-xl">
                <h3 className="font-semibold text-gray-800 mb-2">Выбранная дата:</h3>
                <p className="text-blue-700 font-medium">
                  {selectedDate.toLocaleDateString('ru-RU', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </p>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1">
            <div className="bg-white rounded-2xl shadow-xl p-6 h-full">
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-4">
                  Расписание на {selectedDate.toLocaleDateString('ru-RU', {
                    weekday: 'long',
                    month: 'long',
                    day: 'numeric'
                  })}
                </h2>
                <p className="text-gray-600">
                  Здесь будет отображаться расписание для выбранной даты. 
                  Вы можете добавлять, редактировать и удалять события.
                </p>
              </div>

              {/* Schedule Items */}
              <div className="space-y-4">
                <div className="border-l-4 border-blue-500 pl-4 py-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-gray-800">Математика</h3>
                      <p className="text-gray-600 text-sm">09:00 - 10:30</p>
                    </div>
                    <div className="flex gap-1">
                      <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                        Лекция
                      </span>
                      <span className="bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded-full">
                        Учеба
                      </span>
                    </div>
                  </div>
                </div>

                <div className="border-l-4 border-green-500 pl-4 py-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-gray-800">Физика</h3>
                      <p className="text-gray-600 text-sm">11:00 - 12:30</p>
                    </div>
                    <div className="flex gap-1">
                      <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                        Практика
                      </span>
                      <span className="bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded-full">
                        Учеба
                      </span>
                    </div>
                  </div>
                </div>

                <div className="border-l-4 border-purple-500 pl-4 py-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-gray-800">Информатика</h3>
                      <p className="text-gray-600 text-sm">14:00 - 15:30</p>
                    </div>
                    <div className="flex gap-1">
                      <span className="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded-full">
                        Лабораторная
                      </span>
                      <span className="bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded-full">
                        Учеба
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Empty State */}
              <div className="mt-8 text-center text-gray-500">
                <p>Нет запланированных событий на выбранный день</p>
                <button 
                  onClick={() => setIsModalOpen(true)}
                  className="mt-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors flex items-center mx-auto"
                >
                  <Calendar className="w-4 h-4 mr-2" />
                  Добавить событие
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 relative">
      {/* Account Icon in top right corner */}
      <div className="absolute top-4 right-4 z-10">
        {isAuthenticated ? (
          <div className="relative group">
            <button
              onClick={() => setCurrentPage('account')}
              className="flex items-center space-x-2 bg-white rounded-full shadow-md px-3 py-2 hover:bg-gray-50 transition-colors"
            >
              <div className="bg-blue-500 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium">
                {user.name.charAt(0)}
              </div>
              <span className="text-gray-700 font-medium hidden md:inline-block">{user.name}</span>
            </button>
          </div>
        ) : (
          <div className="flex space-x-2">
            <button
              onClick={() => setCurrentPage('login')}
              className="flex items-center bg-white rounded-lg shadow-md px-4 py-2 hover:bg-gray-50 transition-colors"
            >
              <LogOut className="w-4 h-4 mr-1 text-gray-600" />
              <span className="text-gray-700 font-medium">Войти</span>
            </button>
            <button
              onClick={() => setCurrentPage('register')}
              className="flex items-center bg-blue-500 text-white rounded-lg shadow-md px-4 py-2 hover:bg-blue-600 transition-colors"
            >
              <UserPlus className="w-4 h-4 mr-1" />
              <span className="font-medium hidden sm:inline-block">Регистрация</span>
              <span className="font-medium sm:hidden">Рег.</span>
            </button>
          </div>
        )}
      </div>

      {/* Navigation for mobile */}
      <div className="md:hidden fixed bottom-4 left-1/2 transform -translate-x-1/2 z-20 bg-white rounded-full shadow-lg p-2 flex space-x-6">
        <button
          onClick={() => setCurrentPage('home')}
          className={`p-3 rounded-full transition-colors ${
            currentPage === 'home' ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          <Home className="w-6 h-6" />
        </button>
        <button
          onClick={() => setCurrentPage('account')}
          className={`p-3 rounded-full transition-colors ${
            currentPage === 'account' ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          <User className="w-6 h-6" />
        </button>
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-bold text-gray-800">Добавить событие</h3>
                <button
                  onClick={() => setIsModalOpen(false)}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <X className="w-5 h-5 text-gray-500" />
                </button>
              </div>

              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Event Title */}
                <div>
                  <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
                    <Type className="w-4 h-4 mr-2 text-gray-500" />
                    Название события
                  </label>
                  <input
                    type="text"
                    value={eventData.title}
                    onChange={(e) => handleInputChange('title', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Введите название..."
                    required
                  />
                </div>

                {/* Time Selection */}
                <div>
                  <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
                    <Clock className="w-4 h-4 mr-2 text-gray-500" />
                    Время события
                  </label>
                  <div className="flex items-center space-x-2 mb-2">
                    <input
                      type="checkbox"
                      id="isRange"
                      checked={eventData.isRange}
                      onChange={(e) => handleInputChange('isRange', e.target.checked)}
                      className="rounded text-blue-600 focus:ring-blue-500"
                    />
                    <label htmlFor="isRange" className="text-sm text-gray-600">
                      Диапазон времени (с - до)
                    </label>
                  </div>
                  
                  <div className="flex space-x-2">
                    <input
                      type="time"
                      value={eventData.startTime}
                      onChange={(e) => handleInputChange('startTime', e.target.value)}
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    />
                    {eventData.isRange && (
                      <>
                        <span className="self-center text-gray-500">-</span>
                        <input
                          type="time"
                          value={eventData.endTime}
                          onChange={(e) => handleInputChange('endTime', e.target.value)}
                          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          required
                        />
                      </>
                    )}
                  </div>
                </div>

                {/* Recurring Event */}
                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <input
                      type="checkbox"
                      id="isRecurring"
                      checked={eventData.isRecurring}
                      onChange={(e) => handleInputChange('isRecurring', e.target.checked)}
                      className="rounded text-blue-600 focus:ring-blue-500"
                    />
                    <label htmlFor="isRecurring" className="flex items-center text-sm font-medium text-gray-700">
                      <Repeat className="w-4 h-4 mr-2 text-gray-500" />
                      Регулярное событие?
                    </label>
                  </div>
                  
                  {eventData.isRecurring && (
                    <div className="ml-6 mt-2">
                      <label className="text-sm text-gray-600 mb-1 block">
                        Повторять каждые
                      </label>
                      <div className="flex items-center space-x-2">
                        <input
                          type="number"
                          min="1"
                          value={eventData.recurrenceDays}
                          onChange={(e) => handleInputChange('recurrenceDays', parseInt(e.target.value) || 1)}
                          className="w-20 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <span className="text-sm text-gray-600">дней</span>
                      </div>
                    </div>
                  )}
                </div>

                {/* Reminder */}
                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <input
                      type="checkbox"
                      id="reminder"
                      checked={eventData.reminder}
                      onChange={(e) => handleInputChange('reminder', e.target.checked)}
                      className="rounded text-blue-600 focus:ring-blue-500"
                    />
                    <label htmlFor="reminder" className="flex items-center text-sm font-medium text-gray-700">
                      <Bell className="w-4 h-4 mr-2 text-gray-500" />
                      Предупреждать заранее
                    </label>
                  </div>
                  
                  {eventData.reminder && (
                    <div className="ml-6 mt-2">
                      <label className="text-sm text-gray-600 mb-1 block">
                        За сколько минут
                      </label>
                      <select
                        value={eventData.reminderMinutes}
                        onChange={(e) => handleInputChange('reminderMinutes', parseInt(e.target.value))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value={5}>5 минут</option>
                        <option value={10}>10 минут</option>
                        <option value={15}>15 минут</option>
                        <option value={30}>30 минут</option>
                        <option value={60}>1 час</option>
                        <option value={120}>2 часа</option>
                      </select>
                    </div>
                  )}
                </div>

                {/* Event Color */}
                <div>
                  <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
                    <Palette className="w-4 h-4 mr-2 text-gray-500" />
                    Цвет события
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {colorOptions.map((color) => (
                      <button
                        key={color.value}
                        type="button"
                        onClick={() => handleInputChange('color', color.value)}
                        className={`w-8 h-8 rounded-full border-2 transition-transform hover:scale-110 ${
                          eventData.color === color.value ? 'border-gray-800 scale-110' : 'border-gray-300'
                        }`}
                        style={{ backgroundColor: color.value }}
                        title={color.name}
                      />
                    ))}
                  </div>
                </div>

                {/* Tags */}
                <div>
                  <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
                    <Tag className="w-4 h-4 mr-2 text-gray-500" />
                    Теги
                  </label>
                  
                  {/* Existing Tags */}
                  <div className="flex flex-wrap gap-2 mb-3">
                    {availableTags.map((tag) => (
                      <button
                        key={tag.id}
                        type="button"
                        onClick={() => toggleTag(tag.id)}
                        className={`px-3 py-1 rounded-full text-xs font-medium transition-all ${
                          eventData.tags.includes(tag.id)
                            ? 'ring-2 ring-offset-1 ring-blue-500'
                            : 'opacity-70 hover:opacity-100'
                        }`}
                        style={{ 
                          backgroundColor: tag.color,
                          color: '#ffffff'
                        }}
                      >
                        {tag.name}
                      </button>
                    ))}
                  </div>
                  
                  {/* Create New Tag */}
                  <div className="border-t pt-3">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-gray-600">Создать новый тег</span>
                    </div>
                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={newTagName}
                        onChange={(e) => setNewTagName(e.target.value)}
                        placeholder="Название тега"
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      <div className="flex gap-1">
                        <select
                          value={newTagColor}
                          onChange={(e) => setNewTagColor(e.target.value)}
                          className="px-2 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          {colorOptions.map((color) => (
                            <option key={color.value} value={color.value}>
                              {color.name}
                            </option>
                          ))}
                        </select>
                        <button
                          type="button"
                          onClick={addNewTag}
                          className="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                          disabled={!newTagName.trim()}
                        >
                          <Plus className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Description */}
                <div>
                  <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
                    <Type className="w-4 h-4 mr-2 text-gray-500" />
                    Пояснение к событию
                  </label>
                  <textarea
                    value={eventData.description}
                    onChange={(e) => handleInputChange('description', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                    rows={3}
                    placeholder="Добавьте дополнительные детали..."
                  />
                </div>

                {/* Submit Button */}
                <div className="pt-4">
                  <button
                    type="submit"
                    className="w-full bg-blue-500 text-white py-3 rounded-lg font-medium hover:bg-blue-600 transition-colors focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  >
                    Создать событие
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {renderPageContent()}
    </div>
  );
};

export default ScheduleApp;

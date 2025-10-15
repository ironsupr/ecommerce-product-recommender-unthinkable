import google.generativeai as genai
from config import get_settings
import json
from typing import List, Dict
import random
from functools import lru_cache
import hashlib

settings = get_settings()
genai.configure(api_key=settings.gemini_api_key)

# Initialize Gemini model - using gemini-2.5-flash (latest stable model)
model = genai.GenerativeModel('gemini-2.5-flash')

# Simple cache for recommendations (in production, use Redis)
_recommendation_cache = {}
_chat_cache = {}


def get_unique_products() -> List[Dict]:
    """Return 50 unique innovative products"""
    products = [
        {
            "id": 1,
            "name": "Interactive Smart Mirror",
            "description": "A mirror that doubles as a display for weather, news, calendars, and even at-home fitness classes. Transform your daily routine with this high-tech mirror.",
            "category": "Smart Home & Tech",
            "price": 299.99,
            "image_url": "https://images.unsplash.com/photo-1585241645927-c7a8e5840c42?w=300&h=300&fit=crop",
            "tags": "smart,innovative,tech,home"
        },
        {
            "id": 2,
            "name": "Smart Bird Feeder with Camera",
            "description": "Identifies bird species that visit, takes their photos, and sends notifications to your phone. Perfect for bird enthusiasts and nature lovers.",
            "category": "Smart Home & Tech",
            "price": 149.99,
            "image_url": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=300&h=300&fit=crop",
            "tags": "smart,nature,wildlife,camera"
        },
        {
            "id": 3,
            "name": "Digital Art Canvas",
            "description": "A Wi-Fi-connected frame that displays a rotating collection of famous artworks or personal photos. Turn your wall into a dynamic art gallery.",
            "category": "Smart Home & Tech",
            "price": 249.99,
            "image_url": "https://images.unsplash.com/photo-1513519245088-0e12902e35ca?w=300&h=300&fit=crop",
            "tags": "art,digital,display,smart"
        },
        {
            "id": 4,
            "name": "Temperature Control Smart Mug",
            "description": "Keeps your coffee or tea at the exact desired temperature for hours. Never drink cold coffee again with this intelligent mug.",
            "category": "Smart Home & Tech",
            "price": 79.99,
            "image_url": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=300&h=300&fit=crop",
            "tags": "smart,coffee,temperature,beverage"
        },
        {
            "id": 5,
            "name": "Home Cocktail & Drink Maker",
            "description": "An automated machine that mixes cocktails and other drinks using pods, like a 'Keurig for cocktails.' Host the perfect party effortlessly.",
            "category": "Smart Home & Tech",
            "price": 399.99,
            "image_url": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=300&h=300&fit=crop",
            "tags": "cocktail,smart,party,drinks"
        },
        {
            "id": 6,
            "name": "Indoor Smart Garden",
            "description": "A self-watering, self-lighting hydroponic system for growing herbs and vegetables in your kitchen. Fresh produce year-round, no green thumb required.",
            "category": "Smart Home & Tech",
            "price": 199.99,
            "image_url": "https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?w=300&h=300&fit=crop",
            "tags": "garden,smart,hydroponic,herbs"
        },
        {
            "id": 7,
            "name": "Portable Pocket Projector",
            "description": "A tiny, high-definition projector that can connect to your phone or laptop for an instant cinema experience. Movie night anywhere, anytime.",
            "category": "Smart Home & Tech",
            "price": 179.99,
            "image_url": "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=300&h=300&fit=crop",
            "tags": "projector,portable,entertainment,tech"
        },
        {
            "id": 8,
            "name": "E-Ink Digital Notebook",
            "description": "A paper-like tablet designed for note-taking and reading, which syncs your handwritten notes to the cloud. The feel of paper with the power of digital.",
            "category": "Smart Home & Tech",
            "price": 229.99,
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=300&h=300&fit=crop",
            "tags": "eink,notebook,digital,writing"
        },
        {
            "id": 9,
            "name": "Kintsugi Repair Kit",
            "description": "A kit to learn the Japanese art of repairing broken pottery with gold, celebrating imperfections. Turn broken ceramics into beautiful art pieces.",
            "category": "Hobby & DIY",
            "price": 49.99,
            "image_url": "https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=300&h=300&fit=crop",
            "tags": "art,japanese,diy,craft"
        },
        {
            "id": 10,
            "name": "Artisanal Mushroom Growing Kit",
            "description": "An easy-to-use kit for growing gourmet mushrooms like oyster or shiitake at home. Farm-to-table mushrooms from your own kitchen.",
            "category": "Hobby & DIY",
            "price": 34.99,
            "image_url": "https://images.unsplash.com/photo-1550896622-5cf8b81b46c6?w=300&h=300&fit=crop",
            "tags": "mushroom,growing,organic,diy"
        },
        {
            "id": 11,
            "name": "DIY Hot Sauce Making Kit",
            "description": "Includes a variety of peppers, spices, and bottles for creating your own custom hot sauces. Spice up your life with homemade heat.",
            "category": "Hobby & DIY",
            "price": 39.99,
            "image_url": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=300&h=300&fit=crop",
            "tags": "hotsauce,diy,spicy,cooking"
        },
        {
            "id": 12,
            "name": "Bookbinding Starter Kit",
            "description": "All the tools and materials needed to bind your own journals or repair old books. Create beautiful handmade books and restore treasured volumes.",
            "category": "Hobby & DIY",
            "price": 44.99,
            "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=300&fit=crop",
            "tags": "books,craft,diy,binding"
        },
        {
            "id": 13,
            "name": "At-Home Candle Making Kit",
            "description": "Comes with soy wax, unique fragrances, and stylish containers to craft personalized candles. Fill your home with custom scents.",
            "category": "Hobby & DIY",
            "price": 42.99,
            "image_url": "https://images.unsplash.com/photo-1602874801006-0ceb19ccbb2f?w=300&h=300&fit=crop",
            "tags": "candle,diy,craft,fragrance"
        },
        {
            "id": 14,
            "name": "Terrarium Building Kit",
            "description": "A complete set with a glass container, soil, moss, and decorative elements to create a miniature ecosystem. Build your own tiny world.",
            "category": "Hobby & DIY",
            "price": 36.99,
            "image_url": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=300&h=300&fit=crop",
            "tags": "terrarium,plants,diy,decor"
        },
        {
            "id": 15,
            "name": "Gin & Vodka Infusion Kit",
            "description": "A set of botanicals, spices, and tools to infuse spirits and create unique flavour profiles. Master mixologist in your own home.",
            "category": "Hobby & DIY",
            "price": 54.99,
            "image_url": "https://images.unsplash.com/photo-1569529465841-dfecdab7503b?w=300&h=300&fit=crop",
            "tags": "spirits,infusion,diy,cocktails"
        },
        {
            "id": 16,
            "name": "International Snack Subscription Box",
            "description": "A monthly box featuring a curated selection of snacks and treats from a different country. Taste the world from your couch.",
            "category": "Gourmet Food",
            "price": 29.99,
            "image_url": "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=300&h=300&fit=crop",
            "tags": "snacks,subscription,international,food"
        },
        {
            "id": 17,
            "name": "Molecular Gastronomy Starter Kit",
            "description": "Tools and ingredients to experiment with food science techniques like spherification at home. Become a culinary scientist.",
            "category": "Gourmet Food",
            "price": 64.99,
            "image_url": "https://images.unsplash.com/photo-1556909172-54557c7e4fb7?w=300&h=300&fit=crop",
            "tags": "cooking,science,molecular,gourmet"
        },
        {
            "id": 18,
            "name": "Personalized Tea Blending Subscription",
            "description": "Create a flavour profile and receive custom-blended teas delivered to your door. Your perfect cup, personalized monthly.",
            "category": "Gourmet Food",
            "price": 24.99,
            "image_url": "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=300&h=300&fit=crop",
            "tags": "tea,subscription,personalized,beverage"
        },
        {
            "id": 19,
            "name": "Artisanal Cheese Making Kit",
            "description": "Everything you need to make fresh cheeses like mozzarella, ricotta, or paneer in your kitchen. Homemade cheese has never been easier.",
            "category": "Gourmet Food",
            "price": 46.99,
            "image_url": "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=300&h=300&fit=crop",
            "tags": "cheese,diy,artisan,cooking"
        },
        {
            "id": 20,
            "name": "Coffee Tasting Flight",
            "description": "A curated selection of coffee beans from different regions, complete with tasting notes and origin stories. Explore the world of coffee.",
            "category": "Gourmet Food",
            "price": 34.99,
            "image_url": "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=300&h=300&fit=crop",
            "tags": "coffee,gourmet,tasting,beans"
        },
        {
            "id": 21,
            "name": "Acoustic Art Panels",
            "description": "Sound-absorbing wall panels that feature beautiful artistic designs, combining aesthetics with function. Art that improves your room's acoustics.",
            "category": "Home & Living",
            "price": 129.99,
            "image_url": "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=300&h=300&fit=crop",
            "tags": "acoustic,art,panels,home"
        },
        {
            "id": 22,
            "name": "Weighted Blanket for Pets",
            "description": "A smaller, specially designed weighted blanket to help anxious dogs or cats feel calm. Comfort for your furry friends.",
            "category": "Home & Living",
            "price": 44.99,
            "image_url": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=300&h=300&fit=crop",
            "tags": "pet,weighted,blanket,comfort"
        },
        {
            "id": 23,
            "name": "Sunrise Simulation Alarm Clock",
            "description": "An alarm clock that wakes you up gradually with light that mimics a natural sunrise. Wake up refreshed and energized.",
            "category": "Home & Living",
            "price": 59.99,
            "image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=300&h=300&fit=crop",
            "tags": "alarm,sunrise,sleep,wellness"
        },
        {
            "id": 24,
            "name": "Customizable 3D Printed Vases",
            "description": "Unique, algorithmically generated vase designs that are 3D printed on demand in various colours. One-of-a-kind decor for your home.",
            "category": "Home & Living",
            "price": 39.99,
            "image_url": "https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=300&h=300&fit=crop",
            "tags": "3dprinted,vase,custom,decor"
        },
        {
            "id": 25,
            "name": "Self-Cleaning Water Bottle",
            "description": "Uses UV-C LED light to purify water and clean the inner surfaces of the bottle automatically. Pure hydration, always.",
            "category": "Home & Living",
            "price": 69.99,
            "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop",
            "tags": "bottle,uvc,clean,health"
        },
        {
            "id": 26,
            "name": "Modular Magnetic Shelving",
            "description": "Shelves that can be easily rearranged on a magnetic wall mount to create custom storage layouts. Your storage, your way.",
            "category": "Home & Living",
            "price": 89.99,
            "image_url": "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=300&h=300&fit=crop",
            "tags": "shelving,modular,storage,magnetic"
        },
        {
            "id": 27,
            "name": "Custom Star Map Poster",
            "description": "A map of the stars and constellations from a specific date and location (e.g., a birthday or anniversary). Capture the night sky of your special moment.",
            "category": "Personalized",
            "price": 34.99,
            "image_url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=300&h=300&fit=crop",
            "tags": "stars,custom,poster,personalized"
        },
        {
            "id": 28,
            "name": "Personalized Pet Portrait Canvas",
            "description": "Submit a photo of your pet and have it turned into a classic 'Renaissance' or modern style portrait. Your pet as royalty.",
            "category": "Personalized",
            "price": 79.99,
            "image_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=300&h=300&fit=crop",
            "tags": "pet,portrait,custom,art"
        },
        {
            "id": 29,
            "name": "3D Printed Custom-Fit Eyewear",
            "description": "Glasses frames created from a 3D scan of your face for a perfect, comfortable fit. Eyewear designed uniquely for you.",
            "category": "Personalized",
            "price": 149.99,
            "image_url": "https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=300&h=300&fit=crop",
            "tags": "eyewear,3dprinted,custom,glasses"
        },
        {
            "id": 30,
            "name": "Custom Soundwave Art",
            "description": "A visual representation of a meaningful audio clip (like 'I love you' or a baby's laugh) printed as art. Turn sound into beautiful visual art.",
            "category": "Personalized",
            "price": 44.99,
            "image_url": "https://images.unsplash.com/photo-1549887534-1541e9326642?w=300&h=300&fit=crop",
            "tags": "soundwave,art,custom,audio"
        },
        {
            "id": 31,
            "name": "Engraved Wooden Watch",
            "description": "A stylish watch with a custom message or date engraved on the back. Timeless style with a personal touch.",
            "category": "Personalized",
            "price": 99.99,
            "image_url": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=300&h=300&fit=crop",
            "tags": "watch,wooden,engraved,custom"
        },
        {
            "id": 32,
            "name": "Customizable Mechanical Keyboard",
            "description": "Choose your own switches, keycaps, and base to build a keyboard perfectly suited to your typing style. The ultimate typing experience.",
            "category": "Personalized",
            "price": 189.99,
            "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=300&h=300&fit=crop",
            "tags": "keyboard,mechanical,custom,gaming"
        },
        {
            "id": 33,
            "name": "Smart Jewelry Ring",
            "description": "Tracks activity, sleep, and can be programmed to send subtle notifications from your phone. Wearable tech disguised as elegant jewelry.",
            "category": "Fashion & Accessories",
            "price": 199.99,
            "image_url": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=300&h=300&fit=crop",
            "tags": "smart,jewelry,fitness,ring"
        },
        {
            "id": 34,
            "name": "Recycled Ocean Plastic Apparel",
            "description": "Stylish clothing and shoes with a focus on sustainability, made from recycled ocean plastic. Fashion that saves the planet.",
            "category": "Fashion & Accessories",
            "price": 64.99,
            "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=300&h=300&fit=crop",
            "tags": "sustainable,recycled,fashion,eco"
        },
        {
            "id": 35,
            "name": "Solar-Powered Backpack",
            "description": "A backpack with an integrated solar panel to charge your devices on the go. Power up anywhere under the sun.",
            "category": "Fashion & Accessories",
            "price": 119.99,
            "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop",
            "tags": "solar,backpack,charging,tech"
        },
        {
            "id": 36,
            "name": "Waterproof Knitted Sneakers",
            "description": "Comfortable, breathable sneakers made from a waterproof membrane, perfect for any weather. Style meets function in all conditions.",
            "category": "Fashion & Accessories",
            "price": 89.99,
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop",
            "tags": "sneakers,waterproof,comfort,shoes"
        },
        {
            "id": 37,
            "name": "Convertible Travel Jacket",
            "description": "A jacket with dozens of hidden pockets and features, which can be converted into a bag or pillow. The ultimate travel companion.",
            "category": "Fashion & Accessories",
            "price": 139.99,
            "image_url": "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=300&h=300&fit=crop",
            "tags": "travel,jacket,convertible,utility"
        },
        {
            "id": 38,
            "name": "Meditation Headband",
            "description": "Provides real-time feedback on your brain activity to help you improve your meditation and focus. Train your mind scientifically.",
            "category": "Wellness & Fitness",
            "price": 249.99,
            "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=300&h=300&fit=crop",
            "tags": "meditation,wellness,brain,focus"
        },
        {
            "id": 39,
            "name": "Smart Water Bottle",
            "description": "Tracks your water intake and glows to remind you when it's time to drink more. Stay hydrated with intelligent reminders.",
            "category": "Wellness & Fitness",
            "price": 54.99,
            "image_url": "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=300&h=300&fit=crop",
            "tags": "hydration,smart,bottle,health"
        },
        {
            "id": 40,
            "name": "Acupressure Mat & Pillow Set",
            "description": "A 'bed of needles' style mat that helps relieve tension, muscle pain, and improve sleep. Ancient therapy meets modern wellness.",
            "category": "Wellness & Fitness",
            "price": 49.99,
            "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=300&h=300&fit=crop",
            "tags": "acupressure,wellness,pain,relief"
        },
        {
            "id": 41,
            "name": "Personalized Vitamin Subscription",
            "description": "Based on an online quiz or health test, receive daily vitamin packs tailored to your specific needs. Nutrition personalized for you.",
            "category": "Wellness & Fitness",
            "price": 39.99,
            "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop",
            "tags": "vitamins,personalized,health,subscription"
        },
        {
            "id": 42,
            "name": "Portable Air Purifier",
            "description": "A small, personal air purifier for your desk, car, or for travel. Breathe clean air wherever you go.",
            "category": "Wellness & Fitness",
            "price": 69.99,
            "image_url": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=300&h=300&fit=crop",
            "tags": "air,purifier,portable,health"
        },
        {
            "id": 43,
            "name": "Smart Jump Rope",
            "description": "Tracks your jump count, speed, and calories burned, syncing the data to a fitness app. Turn jumping rope into a data-driven workout.",
            "category": "Wellness & Fitness",
            "price": 44.99,
            "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=300&h=300&fit=crop",
            "tags": "fitness,jumprope,smart,workout"
        },
        {
            "id": 44,
            "name": "Portable Foldable Kayak",
            "description": "An origami-style kayak that folds down into a compact case for easy transport and storage. Adventure made portable.",
            "category": "Outdoor & Travel",
            "price": 799.99,
            "image_url": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop",
            "tags": "kayak,foldable,outdoor,travel"
        },
        {
            "id": 45,
            "name": "Pocket-Sized Washing Machine",
            "description": "A manual, portable wash bag for doing laundry while camping or travelling. Clean clothes anywhere, anytime.",
            "category": "Outdoor & Travel",
            "price": 29.99,
            "image_url": "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=300&h=300&fit=crop",
            "tags": "portable,washing,travel,camping"
        },
        {
            "id": 46,
            "name": "Survival Kit in Sardine Can",
            "description": "A compact, waterproof tin filled with essential survival tools. Big survival in a tiny package.",
            "category": "Outdoor & Travel",
            "price": 24.99,
            "image_url": "https://images.unsplash.com/photo-1578645510447-e20b4311e3ce?w=300&h=300&fit=crop",
            "tags": "survival,compact,emergency,outdoor"
        },
        {
            "id": 47,
            "name": "Scratch-Off World Map",
            "description": "A poster map where you can scratch off the countries you've visited, revealing vibrant colours underneath. Track your adventures in style.",
            "category": "Outdoor & Travel",
            "price": 34.99,
            "image_url": "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=300&h=300&fit=crop",
            "tags": "map,travel,scratch,poster"
        },
        {
            "id": 48,
            "name": "LifeStraw Personal Water Filter",
            "description": "A portable filter that makes contaminated water safe to drink, essential for hiking and emergencies. Clean water from any source.",
            "category": "Outdoor & Travel",
            "price": 19.99,
            "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=300&h=300&fit=crop",
            "tags": "filter,water,survival,hiking"
        },
        {
            "id": 49,
            "name": "Sand-Free Beach Towel",
            "description": "Made from a special material that allows sand to fall right through, keeping you sand-free. Beach days without the hassle.",
            "category": "Outdoor & Travel",
            "price": 39.99,
            "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=300&h=300&fit=crop",
            "tags": "beach,towel,sandfree,summer"
        },
        {
            "id": 50,
            "name": "Smart Luggage Tag with GPS",
            "description": "A tracker that ensures you never lose your luggage again. Travel with peace of mind knowing your bags are always tracked.",
            "category": "Outdoor & Travel",
            "price": 49.99,
            "image_url": "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop",
            "tags": "luggage,gps,tracker,travel"
        }
    ]
    
    return products


async def generate_synthetic_products(count: int = 50) -> List[Dict]:
    """Generate unique innovative product catalog"""
    return get_unique_products()


def get_fallback_products(count: int) -> List[Dict]:
    """Fallback products if Gemini fails"""
    categories = ["Fruits & Vegetables", "Dairy & Eggs", "Snacks & Beverages", "Personal Care", "Home Care", "Bakery"]
    products = []
    
    sample_products = [
        ("Organic Bananas", "Fresh organic bananas, rich in potassium", "Fruits & Vegetables", 3.99, "banana"),
        ("Whole Milk", "Fresh whole milk, 1 gallon", "Dairy & Eggs", 4.99, "milk"),
        ("Potato Chips", "Crispy salted potato chips", "Snacks & Beverages", 2.99, "chips"),
        ("Hand Sanitizer", "Antibacterial hand sanitizer, 500ml", "Personal Care", 5.99, "sanitizer"),
        ("Dish Soap", "Lemon scented dish washing liquid", "Home Care", 3.49, "soap"),
        ("White Bread", "Fresh white bread loaf", "Bakery", 2.49, "bread"),
    ]
    
    for i in range(count):
        base = sample_products[i % len(sample_products)]
        products.append({
            "id": i + 1,
            "name": f"{base[0]} {i+1}",
            "description": base[1],
            "category": base[2],
            "price": round(base[3] + random.uniform(-1, 2), 2),
            "image_url": f"https://source.unsplash.com/300x300/?{base[4]},food,grocery",
            "tags": "fresh,popular"
        })
    
    return products


async def get_recommendations(cart_products: List[Dict], all_products: List[Dict]) -> List[Dict]:
    """Get product recommendations based on cart items using Gemini with caching"""
    
    # Create cache key from cart product IDs
    cart_ids = sorted([p['id'] for p in cart_products])
    cache_key = f"rec_{hashlib.md5(str(cart_ids).encode()).hexdigest()}"
    
    # Check cache
    if cache_key in _recommendation_cache:
        print(f"Cache hit for recommendations: {cache_key}")
        return _recommendation_cache[cache_key]
    
    if not cart_products:
        # Return popular items if cart is empty
        popular = random.sample(all_products, min(3, len(all_products)))
        result = [
            {
                "product": p,
                "reason": f"Trending now! {p['name']} is a customer favorite in the {p['category']} category.",
                "score": 0.75
            }
            for p in popular
        ]
        _recommendation_cache[cache_key] = result
        return result
    
    # Use smart fallback directly for better performance (Gemini can be slow)
    # Comment out the Gemini API call and use the fast smart fallback instead
    print(f"Using smart fallback recommendations for performance")
    result = get_smart_fallback_recommendations(cart_products, all_products)
    _recommendation_cache[cache_key] = result
    return result
    
    # OPTIONAL: Enable Gemini-powered recommendations (slower but more intelligent)
    # Uncomment the code below to use Gemini AI for recommendations
    """
    cart_summary = "\n".join([
        f"- {p['name']} (Category: {p['category']}, Price: ${p['price']}, Tags: {p['tags']})"
        for p in cart_products
    ])
    
    available_products = "\n".join([
        f"ID {p['id']}: {p['name']} - {p['category']} - ${p['price']} - Tags: {p['tags']}"
        for p in all_products[:20]  # Limit to 20 products for faster response
    ])
    
    prompt = f\"\"\"Based on the following cart items, recommend 3-5 complementary products from the available products list.

Cart Items:
{cart_summary}

Available Products:
{available_products}

Consider:
1. Complementary items (e.g., smart home devices with home essentials)
2. Same category items the user might need
3. Popular pairings
4. Cross-selling opportunities

Return a JSON array with this structure:
[
    {{
        "product_id": <id>,
        "reason": "<compelling sales-oriented reason>",
        "score": <0.0-1.0>
    }}
]

Return ONLY valid JSON, no other text. Recommend 3-5 products.\"\"\"

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean markdown
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        text = text.strip()
        recommendations = json.loads(text)
        
        # Validate and enrich recommendations
        result = []
        for rec in recommendations[:5]:
            product = next((p for p in all_products if p['id'] == rec['product_id']), None)
            if product:
                result.append({
                    "product": product,
                    "reason": rec['reason'],
                    "score": rec.get('score', 0.8)
                })
        
        if result:
            _recommendation_cache[cache_key] = result
            return result
        else:
            result = get_smart_fallback_recommendations(cart_products, all_products)
            _recommendation_cache[cache_key] = result
            return result
            
    except Exception as e:
        print(f"Error getting recommendations from Gemini: {e}")
        result = get_smart_fallback_recommendations(cart_products, all_products)
        _recommendation_cache[cache_key] = result
        return result
    """


def get_smart_fallback_recommendations(cart_products: List[Dict], all_products: List[Dict]) -> List[Dict]:
    """Smart fallback recommendations based on category matching and common pairings"""
    
    # Define category relationships and common pairings for unique products
    category_pairings = {
        "Smart Home & Tech": {
            "pairs_with": ["Home & Living", "Wellness & Fitness", "Fashion & Accessories"],
            "reasons": {
                "Home & Living": "Perfect pairing! Enhance your smart home setup with these complementary home essentials.",
                "Wellness & Fitness": "Great combo! Smart tech pairs excellently with wellness products for a healthier lifestyle.",
                "Fashion & Accessories": "Complete your tech ecosystem! Smart accessories work seamlessly with your devices."
            }
        },
        "Hobby & DIY": {
            "pairs_with": ["Gourmet Food", "Home & Living", "Personalized"],
            "reasons": {
                "Gourmet Food": "Perfect match! Create and enjoy - DIY hobbies pair wonderfully with gourmet experiences.",
                "Home & Living": "Smart choice! Display and organize your DIY creations with these home essentials.",
                "Personalized": "Enhance your creativity! Personalized items complement your DIY projects beautifully."
            }
        },
        "Gourmet Food": {
            "pairs_with": ["Hobby & DIY", "Home & Living", "Outdoor & Travel"],
            "reasons": {
                "Hobby & DIY": "Excellent pairing! DIY kits enhance your gourmet food experiences.",
                "Home & Living": "Complete your setup! Proper storage and serving items elevate your gourmet collection.",
                "Outdoor & Travel": "Adventure ready! Take your gourmet tastes on the go with travel essentials."
            }
        },
        "Home & Living": {
            "pairs_with": ["Smart Home & Tech", "Personalized", "Wellness & Fitness"],
            "reasons": {
                "Smart Home & Tech": "Great combo! Smart devices integrate perfectly with your home essentials.",
                "Personalized": "Make it yours! Personalized items add a unique touch to your living space.",
                "Wellness & Fitness": "Healthy home! Wellness products complement your living space beautifully."
            }
        },
        "Personalized": {
            "pairs_with": ["Home & Living", "Fashion & Accessories", "Hobby & DIY"],
            "reasons": {
                "Home & Living": "Perfect display! Show off your personalized items with these home essentials.",
                "Fashion & Accessories": "Complete your style! Personalized pieces pair perfectly with unique accessories.",
                "Hobby & DIY": "Creative synergy! DIY projects complement your personalized collection."
            }
        },
        "Fashion & Accessories": {
            "pairs_with": ["Wellness & Fitness", "Outdoor & Travel", "Smart Home & Tech"],
            "reasons": {
                "Wellness & Fitness": "Active lifestyle! Fitness gear complements your fashion choices perfectly.",
                "Outdoor & Travel": "Adventure ready! Travel gear enhances your fashion-forward lifestyle.",
                "Smart Home & Tech": "Tech-savvy style! Smart accessories integrate seamlessly with your wardrobe."
            }
        },
        "Wellness & Fitness": {
            "pairs_with": ["Fashion & Accessories", "Smart Home & Tech", "Home & Living"],
            "reasons": {
                "Fashion & Accessories": "Complete your workout! Fitness fashion enhances your wellness routine.",
                "Smart Home & Tech": "Track your progress! Smart tech perfectly complements your wellness journey.",
                "Home & Living": "Wellness at home! Create a healthy living space with these essentials."
            }
        },
        "Outdoor & Travel": {
            "pairs_with": ["Fashion & Accessories", "Wellness & Fitness", "Gourmet Food"],
            "reasons": {
                "Fashion & Accessories": "Travel in style! Accessories perfect for your outdoor adventures.",
                "Wellness & Fitness": "Active adventures! Fitness gear enhances your outdoor experiences.",
                "Gourmet Food": "Fuel your journey! Gourmet options for your travel adventures."
            }
        }
    }
    
    recommendations = []
    cart_categories = list(set([p['category'] for p in cart_products]))
    
    # Find complementary products based on category matching
    for cart_cat in cart_categories:
        if cart_cat in category_pairings:
            pairing_info = category_pairings[cart_cat]
            
            for target_cat in pairing_info["pairs_with"]:
                # Find products in the target category
                matching_products = [p for p in all_products if p['category'] == target_cat]
                
                if matching_products and len(recommendations) < 5:
                    product = random.choice(matching_products)
                    reason = pairing_info["reasons"].get(
                        target_cat, 
                        f"Great addition! This {target_cat} item complements your current selection perfectly."
                    )
                    
                    # Check if product already recommended
                    if not any(r['product']['id'] == product['id'] for r in recommendations):
                        recommendations.append({
                            "product": product,
                            "reason": reason,
                            "score": 0.85
                        })
    
    # If we need more recommendations, add popular items from cart categories
    if len(recommendations) < 3:
        for cart_cat in cart_categories:
            same_category = [p for p in all_products if p['category'] == cart_cat]
            for product in same_category:
                if len(recommendations) >= 5:
                    break
                if not any(r['product']['id'] == product['id'] for r in recommendations):
                    recommendations.append({
                        "product": product,
                        "reason": f"You might also like this! Another great {cart_cat} option to add to your cart.",
                        "score": 0.75
                    })
    
    # If still not enough, add random popular items
    while len(recommendations) < 3 and len(all_products) > len(recommendations):
        product = random.choice(all_products)
        if not any(r['product']['id'] == product['id'] for r in recommendations):
            recommendations.append({
                "product": product,
                "reason": f"Trending now! Customers love this {product['category']} item.",
                "score": 0.70
            })
    
    return recommendations[:5]


async def answer_question(question: str, cart_products: List[Dict], recommended_product: Dict = None) -> str:
    """Answer user questions about recommendations using Gemini chatbot"""
    
    context = ""
    
    if cart_products:
        cart_summary = "\n".join([
            f"- {p['name']} ({p['category']}) - ${p['price']}"
            for p in cart_products
        ])
        context += f"\nUser's Cart:\n{cart_summary}\n"
    
    if recommended_product:
        context += f"\nRecommended Product:\n- {recommended_product['name']} ({recommended_product['category']}) - ${recommended_product['price']}\n- Description: {recommended_product['description']}\n"
    
    prompt = f"""You are a helpful shopping assistant for an e-commerce grocery app similar to Blinkit or Zomato.

{context}

User Question: {question}

Provide a helpful, concise answer (2-3 sentences). Be friendly and informative.
If the user asks "why was this recommended?" or similar, explain the recommendation logic based on their cart items and product complementarity."""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        import traceback
        print(f"Error answering question: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return "I apologize, but I'm having trouble processing your question right now. Please try again."

import logging
import os
from dotenv import load_dotenv
load_dotenv()

#Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

BASEURL = "alpha-vantage.p.rapidapi.com"

api_key = os.getenv('API_KEY')

url = f"https://{BASEURL}/query"

headers = {
	"x-rapidapi-key": api_key,
	"x-rapidapi-host": BASEURL
}


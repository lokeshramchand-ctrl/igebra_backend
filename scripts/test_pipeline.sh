#!/bin/bash

BASE_URL="http://localhost:8080"

echo -e "\n============================================="
echo "  VELAR TRANSACTION ENGINE - E2E TEST "
echo -e "=============================================\n"

echo -e "--- PHASE 3: MERCHANT RESOLUTION ---"
echo "Sending noisy UPI string: 'UPI/CR/3152671239/BUNDL TECHNOLOGIES/HDFC'"
curl -s -X POST "$BASE_URL/v1/resolve" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"UPI/CR/3152671239/BUNDL TECHNOLOGIES/HDFC\"}"
echo -e "\n\n"
sleep 1

echo -e "--- PHASE 4: MEMORY ENGINE (STATE PROMOTION) ---"
echo "Simulating 3 transactions for a new entity 'Zomato' to trigger TEMPORARY state."
for i in {1..3}
do
   echo "Encounter $i:"
   curl -s -X POST "$BASE_URL/memory/update" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d "{\"canonical_name\": \"Zomato\", \"raw_text\": \"paid to zomato media pvt\"}"
   echo -e "\n"
done
echo -e "\n"
sleep 1

echo -e "--- PHASE 5: CONFIDENCE WALL ---"
echo "Evaluating a low-confidence ML prediction (Confidence: 0.40). Should route to UNKNOWN."
curl -s -X POST "$BASE_URL/v1/confidence/evaluate" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{\"predicted_category\": \"Travel\", \"raw_confidence\": 0.40}"
echo -e "\n\n"
sleep 1

echo -e "--- PHASE 13: ANALYTICS ENGINE ---"
echo "Fetching top merchants (Should include our newly added test data)."
curl -s -X GET "$BASE_URL/v1/analytics/patterns/merchants?limit=5" \
  -H "accept: application/json"
echo -e "\n\n"

echo -e "============================================="
echo "  TEST COMPLETE"
echo -e "=============================================\n"

"""Generate golden evaluation set for Uber CS Agent."""

import json
from pathlib import Path


def generate_golden_set():
    """Generate 150+ labeled examples for evaluation."""

    golden_examples = []

    trip_issue_examples = [
        {"query": "My driver took a really long route and I was charged way more than usual", "intent": "trip_issue", "should_escalate": False},
        {"query": "The driver went the wrong way and added 20 minutes to my trip", "intent": "trip_issue", "should_escalate": False},
        {"query": "Driver took unnecessary detours and my fare is double what it should be", "intent": "trip_issue", "should_escalate": False},
        {"query": "The route was completely inefficient, went through side streets instead of highway", "intent": "trip_issue", "should_escalate": False},
        {"query": "My trip should have been 15 mins but driver took 40 mins and charged me extra", "intent": "trip_issue", "should_escalate": False},
        {"query": "Driver missed my destination and drove in circles for 10 minutes", "intent": "trip_issue", "should_escalate": False},
        {"query": "GPS route was completely wrong and cost me an extra $15", "intent": "trip_issue", "should_escalate": False},
        {"query": "The driver deliberately took a longer route to increase the fare", "intent": "trip_issue", "should_escalate": False},
        {"query": "Route took me through tolls when there was a free route available", "intent": "trip_issue", "should_escalate": False},
        {"query": "Trip was supposed to be $25 but ended up being $42 due to wrong route", "intent": "trip_issue", "should_escalate": False},
        {"query": "My driver got lost multiple times and I ended up paying double", "intent": "trip_issue", "should_escalate": False},
        {"query": "The estimated route was 10 miles but actual trip was 18 miles", "intent": "trip_issue", "should_escalate": False},
        {"query": "Driver ignored GPS and took their own route which was much longer", "intent": "trip_issue", "should_escalate": False},
        {"query": "I was charged for sitting in traffic when driver took a congested route", "intent": "trip_issue", "should_escalate": False},
        {"query": "Trip route doesn't match what GPS shows, need fare adjustment", "intent": "trip_issue", "should_escalate": False},
    ]

    payment_examples = [
        {"query": "My credit card was declined but I know it has funds", "intent": "payment", "should_escalate": False},
        {"query": "I was charged twice for the same ride", "intent": "payment", "should_escalate": False},
        {"query": "Payment method keeps failing even though card is valid", "intent": "payment", "should_escalate": False},
        {"query": "I see a $50 charge on my card that I don't recognize", "intent": "payment", "should_escalate": False},
        {"query": "How do I update my payment information?", "intent": "payment", "should_escalate": False},
        {"query": "My bank says Uber charged me $120 but app shows $80", "intent": "payment", "should_escalate": False},
        {"query": "Need to add a different credit card for payment", "intent": "payment", "should_escalate": False},
        {"query": "I was charged even though I cancelled before the trip started", "intent": "payment", "should_escalate": False},
        {"query": "Double charge appeared on my statement for trip yesterday", "intent": "payment", "should_escalate": False},
        {"query": "Payment is showing as pending for 3 days now", "intent": "payment", "should_escalate": False},
        {"query": "Can I split payment between two cards?", "intent": "payment", "should_escalate": False},
        {"query": "Uber Cash not being applied to my rides", "intent": "payment", "should_escalate": False},
        {"query": "I was charged international fees when I'm in my home country", "intent": "payment", "should_escalate": False},
        {"query": "Need receipt for business expense, payment amount seems wrong", "intent": "payment", "should_escalate": False},
        {"query": "My card expired and I can't book rides now", "intent": "payment", "should_escalate": False},
    ]

    account_examples = [
        {"query": "How do I change my email address?", "intent": "account", "should_escalate": False},
        {"query": "I forgot my password and reset link isn't working", "intent": "account", "should_escalate": False},
        {"query": "Need to update my phone number on account", "intent": "account", "should_escalate": False},
        {"query": "Can't log in to my account anymore", "intent": "account", "should_escalate": False},
        {"query": "How do I change my profile name?", "intent": "account", "should_escalate": False},
        {"query": "I want to delete my Uber account permanently", "intent": "account", "should_escalate": False},
        {"query": "My account was locked and I don't know why", "intent": "account", "should_escalate": False},
        {"query": "Need to verify my email address but didn't receive the code", "intent": "account", "should_escalate": False},
        {"query": "How do I add a profile picture?", "intent": "account", "should_escalate": False},
        {"query": "Can I have multiple Uber accounts with same phone?", "intent": "account", "should_escalate": False},
        {"query": "I want to change my account settings for notifications", "intent": "account", "should_escalate": False},
        {"query": "My account shows wrong name, need to update it", "intent": "account", "should_escalate": False},
        {"query": "How do I switch between personal and business profiles?", "intent": "account", "should_escalate": False},
        {"query": "Account login page keeps giving error message", "intent": "account", "should_escalate": False},
        {"query": "I need to update my home address in account settings", "intent": "account", "should_escalate": False},
    ]

    safety_examples = [
        {"query": "Driver was driving recklessly and I felt unsafe", "intent": "safety", "should_escalate": True},
        {"query": "The driver ran multiple red lights during my trip", "intent": "safety", "should_escalate": True},
        {"query": "I was in an accident during my Uber ride", "intent": "safety", "should_escalate": True},
        {"query": "Driver was texting while driving the entire time", "intent": "safety", "should_escalate": True},
        {"query": "The driver made inappropriate comments and I felt threatened", "intent": "safety", "should_escalate": True},
        {"query": "Emergency: driver is driving dangerously and won't stop", "intent": "safety", "should_escalate": True},
        {"query": "Driver was speeding excessively, going 90 in a 55 zone", "intent": "safety", "should_escalate": True},
        {"query": "I felt unsafe because driver was clearly intoxicated", "intent": "safety", "should_escalate": True},
        {"query": "Driver made me very uncomfortable with personal questions", "intent": "safety", "should_escalate": True},
        {"query": "The car had no working seatbelts in the back", "intent": "safety", "should_escalate": True},
        {"query": "Driver took me to a different location than requested and refused to leave", "intent": "safety", "should_escalate": True},
        {"query": "I need to report a safety incident from my last trip", "intent": "safety", "should_escalate": True},
        {"query": "Driver was aggressive and yelling at other drivers", "intent": "safety", "should_escalate": True},
        {"query": "The driver's behavior made me fear for my safety", "intent": "safety", "should_escalate": True},
        {"query": "Need emergency assistance, driver won't let me out of car", "intent": "safety", "should_escalate": True},
    ]

    driver_issue_examples = [
        {"query": "Driver was extremely rude and yelled at me", "intent": "driver_issue", "should_escalate": True},
        {"query": "The driver refused to help with my luggage", "intent": "driver_issue", "should_escalate": True},
        {"query": "Driver was unprofessional and complained entire trip", "intent": "driver_issue", "should_escalate": True},
        {"query": "My driver was on phone calls the whole ride ignoring me", "intent": "driver_issue", "should_escalate": True},
        {"query": "Driver refused to turn down loud music when I asked", "intent": "driver_issue", "should_escalate": True},
        {"query": "The driver was rude when I asked to make a quick stop", "intent": "driver_issue", "should_escalate": True},
        {"query": "Driver complained about my destination being too far", "intent": "driver_issue", "should_escalate": True},
        {"query": "The driver refused to let me bring my service dog", "intent": "driver_issue", "should_escalate": True},
        {"query": "Driver was eating and didn't greet or acknowledge me", "intent": "driver_issue", "should_escalate": True},
        {"query": "The driver asked for cash payment outside the app", "intent": "driver_issue", "should_escalate": True},
        {"query": "Driver was very unprofessional and made me uncomfortable", "intent": "driver_issue", "should_escalate": True},
        {"query": "My driver cancelled after I got in the car and demanded cash", "intent": "driver_issue", "should_escalate": True},
        {"query": "Driver refused pickup because of my wheelchair", "intent": "driver_issue", "should_escalate": True},
        {"query": "The driver was smoking in the car during my trip", "intent": "driver_issue", "should_escalate": True},
        {"query": "Driver made discriminatory comments during the ride", "intent": "driver_issue", "should_escalate": True},
    ]

    cancellation_examples = [
        {"query": "Why was I charged a cancellation fee?", "intent": "cancellation", "should_escalate": False},
        {"query": "I cancelled because driver was taking too long", "intent": "cancellation", "should_escalate": False},
        {"query": "Cancellation fee of $7 seems unfair, driver never moved", "intent": "cancellation", "should_escalate": False},
        {"query": "How long do I have to cancel without being charged?", "intent": "cancellation", "should_escalate": False},
        {"query": "Driver cancelled on me after 10 minute wait", "intent": "cancellation", "should_escalate": False},
        {"query": "I was charged even though I cancelled immediately", "intent": "cancellation", "should_escalate": False},
        {"query": "Can I get refund on cancellation fee? Driver went wrong direction", "intent": "cancellation", "should_escalate": False},
        {"query": "Multiple cancellation fees in one day, this is excessive", "intent": "cancellation", "should_escalate": False},
        {"query": "Driver cancelled but I still got charged cancellation fee", "intent": "cancellation", "should_escalate": False},
        {"query": "Why am I paying cancellation fee when driver was 15 mins late?", "intent": "cancellation", "should_escalate": False},
        {"query": "Cancelled due to emergency but still charged, need refund", "intent": "cancellation", "should_escalate": False},
        {"query": "What is your cancellation policy?", "intent": "cancellation", "should_escalate": False},
        {"query": "Driver cancelled three times in a row on me", "intent": "cancellation", "should_escalate": False},
        {"query": "Unfair cancellation charge when I waited 10 minutes", "intent": "cancellation", "should_escalate": False},
        {"query": "I cancelled within 2 minutes but still got fee", "intent": "cancellation", "should_escalate": False},
    ]

    refund_examples = [
        {"query": "I need a refund for my last trip", "intent": "refund", "should_escalate": False},
        {"query": "Can I get my money back for this overcharge?", "intent": "refund", "should_escalate": False},
        {"query": "Requesting refund of $15 for wrong route", "intent": "refund", "should_escalate": False},
        {"query": "I was charged for a trip I never took, need full refund", "intent": "refund", "should_escalate": False},
        {"query": "Refund request for $25, driver never showed up", "intent": "refund", "should_escalate": False},
        {"query": "How do I get reimbursed for this incorrect charge?", "intent": "refund", "should_escalate": False},
        {"query": "I need a refund of $80 for fraudulent cleaning fee", "intent": "refund", "should_escalate": True},
        {"query": "Can you refund the difference between estimate and actual fare?", "intent": "refund", "should_escalate": False},
        {"query": "Requesting $10 refund for poor service", "intent": "refund", "should_escalate": False},
        {"query": "I deserve a refund, this ride was terrible", "intent": "refund", "should_escalate": False},
        {"query": "Please refund my cancellation fee of $7", "intent": "refund", "should_escalate": False},
        {"query": "I want my money back for this trip immediately", "intent": "refund", "should_escalate": False},
        {"query": "Need $120 refund for surge pricing during outage", "intent": "refund", "should_escalate": True},
        {"query": "Can I get partial refund? Trip was not as expected", "intent": "refund", "should_escalate": False},
        {"query": "Refund needed for double charge of $45", "intent": "refund", "should_escalate": False},
    ]

    app_bug_examples = [
        {"query": "The app keeps crashing when I try to book a ride", "intent": "app_bug", "should_escalate": False},
        {"query": "Map is not loading, just shows blank screen", "intent": "app_bug", "should_escalate": False},
        {"query": "App freezes every time I open it", "intent": "app_bug", "should_escalate": False},
        {"query": "Can't request rides, app says error occurred", "intent": "app_bug", "should_escalate": False},
        {"query": "The app is not showing any available drivers", "intent": "app_bug", "should_escalate": False},
        {"query": "Payment screen won't load when I try to add card", "intent": "app_bug", "should_escalate": False},
        {"query": "App crashes immediately after opening on my iPhone", "intent": "app_bug", "should_escalate": False},
        {"query": "Location services not working in the app", "intent": "app_bug", "should_escalate": False},
        {"query": "Bug: can't see trip history, page is blank", "intent": "app_bug", "should_escalate": False},
        {"query": "The app glitches when I try to schedule a ride", "intent": "app_bug", "should_escalate": False},
        {"query": "Uber app won't let me sign in, keeps saying error", "intent": "app_bug", "should_escalate": False},
        {"query": "App is stuck on loading screen", "intent": "app_bug", "should_escalate": False},
        {"query": "Driver tracking isn't working, map frozen", "intent": "app_bug", "should_escalate": False},
        {"query": "The app logged me out and won't let me back in", "intent": "app_bug", "should_escalate": False},
        {"query": "Getting 'something went wrong' error constantly", "intent": "app_bug", "should_escalate": False},
    ]

    promo_examples = [
        {"query": "My promo code isn't working", "intent": "promo", "should_escalate": False},
        {"query": "I entered code SAVE20 but it didn't apply discount", "intent": "promo", "should_escalate": False},
        {"query": "Promo code says invalid but I just received it via email", "intent": "promo", "should_escalate": False},
        {"query": "How do I use my referral credit?", "intent": "promo", "should_escalate": False},
        {"query": "First ride discount didn't apply to my trip", "intent": "promo", "should_escalate": False},
        {"query": "Where do I enter promo codes in the app?", "intent": "promo", "should_escalate": False},
        {"query": "My $10 credit disappeared from my account", "intent": "promo", "should_escalate": False},
        {"query": "Promo code FRIEND15 not being accepted", "intent": "promo", "should_escalate": False},
        {"query": "I was supposed to get 50% off but was charged full price", "intent": "promo", "should_escalate": False},
        {"query": "Do you have any current promotions or discounts?", "intent": "promo", "should_escalate": False},
        {"query": "My new user promo didn't work on first ride", "intent": "promo", "should_escalate": False},
        {"query": "How long do promo codes last before expiring?", "intent": "promo", "should_escalate": False},
        {"query": "Discount code from partner company isn't applying", "intent": "promo", "should_escalate": False},
        {"query": "Can I combine multiple promo codes?", "intent": "promo", "should_escalate": False},
        {"query": "The promo worked on first trip but not second", "intent": "promo", "should_escalate": False},
    ]

    eta_wait_examples = [
        {"query": "My driver has been 5 minutes away for 20 minutes", "intent": "eta_wait", "should_escalate": False},
        {"query": "Driver ETA keeps increasing instead of decreasing", "intent": "eta_wait", "should_escalate": False},
        {"query": "I've been waiting 30 minutes and driver still isn't here", "intent": "eta_wait", "should_escalate": False},
        {"query": "The app said 3 minutes but it's been 15 minutes", "intent": "eta_wait", "should_escalate": False},
        {"query": "Driver is going in wrong direction, when will they arrive?", "intent": "eta_wait", "should_escalate": False},
        {"query": "How much longer? Driver has been circling for 10 minutes", "intent": "eta_wait", "should_escalate": False},
        {"query": "Very long wait time, is my driver actually coming?", "intent": "eta_wait", "should_escalate": False},
        {"query": "Driver is 15 minutes late from estimated arrival", "intent": "eta_wait", "should_escalate": False},
        {"query": "Why is my driver just sitting in one place?", "intent": "eta_wait", "should_escalate": False},
        {"query": "Waited over 20 minutes, driver never showed up", "intent": "eta_wait", "should_escalate": False},
        {"query": "ETA was 2 mins but driver is now 8 mins away", "intent": "eta_wait", "should_escalate": False},
        {"query": "My driver isn't moving towards pickup location", "intent": "eta_wait", "should_escalate": False},
        {"query": "How long do I have to wait before I can cancel?", "intent": "eta_wait", "should_escalate": False},
        {"query": "Driver keeps stopping and ETA keeps going up", "intent": "eta_wait", "should_escalate": False},
        {"query": "Been waiting 40 minutes, this is unacceptable", "intent": "eta_wait", "should_escalate": False},
    ]

    other_examples = [
        {"query": "How do I schedule a ride for tomorrow?", "intent": "other", "should_escalate": False},
        {"query": "I left my phone in the car, how do I contact driver?", "intent": "other", "should_escalate": False},
        {"query": "Can I request a specific driver?", "intent": "other", "should_escalate": False},
        {"query": "What's the difference between UberX and UberXL?", "intent": "other", "should_escalate": False},
        {"query": "How do I add a stop to my trip?", "intent": "other", "should_escalate": False},
        {"query": "Do you operate in my city?", "intent": "other", "should_escalate": False},
        {"query": "Can I bring my pet in an Uber?", "intent": "other", "should_escalate": False},
        {"query": "How do I get receipts for my rides?", "intent": "other", "should_escalate": False},
        {"query": "What are your business account options?", "intent": "other", "should_escalate": False},
        {"query": "I want to become an Uber driver", "intent": "other", "should_escalate": False},
        {"query": "How do I tip my driver?", "intent": "other", "should_escalate": False},
        {"query": "Can I share my ride location with someone?", "intent": "other", "should_escalate": False},
        {"query": "What is your accessibility policy?", "intent": "other", "should_escalate": False},
        {"query": "Do you have a rewards program?", "intent": "other", "should_escalate": False},
        {"query": "How does surge pricing work?", "intent": "other", "should_escalate": False},
    ]

    golden_examples.extend(trip_issue_examples)
    golden_examples.extend(payment_examples)
    golden_examples.extend(account_examples)
    golden_examples.extend(safety_examples)
    golden_examples.extend(driver_issue_examples)
    golden_examples.extend(cancellation_examples)
    golden_examples.extend(refund_examples)
    golden_examples.extend(app_bug_examples)
    golden_examples.extend(promo_examples)
    golden_examples.extend(eta_wait_examples)
    golden_examples.extend(other_examples)

    return golden_examples


if __name__ == "__main__":
    golden_set = generate_golden_set()

    output_path = Path(__file__).parent.parent / "evals" / "golden" / "golden_set.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(golden_set, f, indent=2)

    print(f"Generated {len(golden_set)} golden examples")
    print(f"Saved to: {output_path}")

    intent_counts = {}
    for ex in golden_set:
        intent = ex["intent"]
        intent_counts[intent] = intent_counts.get(intent, 0) + 1

    print("\nIntent distribution:")
    for intent, count in sorted(intent_counts.items()):
        escalate_count = sum(1 for ex in golden_set if ex["intent"] == intent and ex.get("should_escalate", False))
        print(f"  {intent}: {count} ({escalate_count} escalations)")

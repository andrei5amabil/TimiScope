# TimiScope

**A living map of what's happening in Timișoara.**

TimiScope is a community-driven platform that helps people explore, report, and understand events across Timișoara. From damaged sidewalks and overflowing bins to local markets and public events, TimiScope brings useful local information together on one interactive map.

The goal is to build a shared digital picture of the city—not a 3D reconstruction or a simulation, but a continuously updated view shaped by what people observe and what is happening around them.

> **Project status:** Early development. The features described here are planned goals, not claims that the application is already fully implemented.

## Why TimiScope?

Information about a city is often scattered across social media posts, group chats, websites, and individual reports. It can be difficult to tell what is happening nearby, whether other people have reported the same issue, or where particular problems keep appearing.

TimiScope aims to make that information easier to find and understand. People can explore events on a map, contribute observations, and see related reports brought together. Over time, the collected information may also reveal patterns across neighborhoods and time periods.

## How it works

1. **Explore the city.** Browse an interactive map of Timișoara and filter what appears by event type, category, time, and status.
2. **Report what you see.** Personal users can report problems, add a description, and mark the location. Report photos must be taken using the camera inside the app; the report flow will not offer photo selection from the device gallery.
3. **Bring related reports together.** When several people report the same issue, TimiScope can use AI to suggest that the reports refer to one event, while preserving the original observations.
4. **Review and understand.** Moderation and verification workflows help users understand what has been reviewed, while map layers and heatmaps show where reports are concentrated.
5. **Discover positive events.** Verified businesses can publish upcoming events they organize, such as markets, performances, or community activities.

## What appears on the map?

TimiScope distinguishes between the **kind of event** and its **subject category**.

- **Problems:** Things that may need attention, such as potholes, broken streetlights, blocked sidewalks, or overflowing bins.
- **Positive events:** Upcoming activities and events organized by verified businesses, such as concerts, markets, or community gatherings.
- **Informational events:** A possible future category for useful local information, if it fits the project scope.

Categories describe the subject—for example, infrastructure, mobility, environment, public spaces, or community activities. Users can filter the map to focus on what matters to them. Different event types will use distinct colors and symbols so that the map is easier to scan.

## Who is it for?

### Personal users

Residents and visitors can browse the map and submit observations about problems around the city. They can see whether a report is awaiting review or has been connected to a broader event.

### Businesses and event organizers

Businesses can apply for verification. Once approved, they can publish and manage upcoming positive events they organize. Verification confirms the organizer's account status; it does not automatically guarantee every detail of an event listing.

### Administrators

Administrators review business verification applications, moderate reports and event listings, and assess AI-suggested report matches. Important moderation decisions should be recorded so they can be understood later.

## How AI helps

A central challenge is figuring out whether two reports describe the same real-world occurrence. One person might report a pothole as “road damage,” while another describes “a large hole near the crossing.” A map based only on individual submissions could show these as separate items even when they refer to the same problem.

TimiScope will investigate whether AI can compare report descriptions and, when available, photos to suggest likely duplicates. The system can also consider whether reports are close in location and time. These suggestions can help reduce clutter and make reports more useful together.

**AI is an assistant, not a source of truth.** Similarity scores do not prove that two reports match, and a photo cannot by itself establish that a claim is true or current. Uncertain cases should remain separate or be sent for human review rather than being merged without appropriate safeguards.

## Understanding city-wide patterns

TimiScope will provide more than individual map markers. Users should be able to explore clusters of nearby events and heatmaps showing concentrations of reports for selected categories and time periods.

These visualizations can help people spot patterns—for example, areas where infrastructure problems are reported more frequently. They must be interpreted carefully: a high concentration means more reports in the selected data, not necessarily greater danger, and an area with few reports is not proof that no problems exist there.

## Trust, privacy, and responsible use

TimiScope is intended to be useful without overstating what it knows. Key principles include:

- **Keep original observations:** Linking reports together should not erase the original descriptions or evidence.
- **Make review status clear:** Users should be able to distinguish unreviewed information from information that has received moderator review.
- **Protect uploaded content:** Photos and business verification documents should be handled with appropriate access restrictions.
- **Reduce opportunities for photo abuse:** Problem-report photos will be captured through the in-app camera flow instead of selected from the gallery. This raises the barrier to reusing old images, but cannot prove that a photo is genuine or shows the reported location.
- **Use moderation and audit history:** Reports, listings, and consequential decisions need appropriate review and abuse-handling processes.
- **Do not replace emergency services:** TimiScope is not an emergency reporting or dispatch service. Immediate danger should be reported through official emergency channels.

## Project and research goals

TimiScope is also a bachelor's thesis project. Beyond building a usable application, it will evaluate whether AI-assisted matching improves on simpler methods that compare report location, time, and category.

The evaluation will focus on both useful matches and harmful mistakes. Incorrectly merging two separate events can hide important information, while failing to connect duplicate reports can leave the map cluttered. The project aims to measure these trade-offs and document the limits of the results, especially if the available dataset is small.

## Planned direction

The initial focus is Timișoara and a manageable set of event categories. The first usable version is expected to bring together:

- An interactive city map with event filters.
- Problem reporting with location, description, and in-app camera capture.
- Positive event listings for verified business accounts.
- AI-assisted duplicate suggestions with human review for uncertain cases.
- Basic moderation and verification tools.
- Map clusters, heatmaps, and a documented evaluation of matching quality.

A full 3D city reconstruction, traffic simulation, automatic verification of real-world truth, and guaranteed integration with municipal systems are outside the initial scope.

## Technology

The planned implementation uses a React-based web interface, a React Native mobile app, a Python API, and a geospatial database. AI capabilities will be evaluated using suitable pretrained models. The specific components may change as the project is developed and tested.

---

**TimiScope aims to make Timișoara easier to understand through shared observations, clearer local information, and a map that shows not only where things are, but what people are reporting about the city.**
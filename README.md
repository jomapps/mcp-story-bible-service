# MCP Story Bible Service

**Purpose**: Comprehensive story bible creation and management service for the AI Movie Generation Platform.

## Overview

The MCP Story Bible Service is a specialized Model Context Protocol (MCP) server designed to create, manage, and maintain comprehensive story bibles for movie projects. It handles narrative structure, character development, scene management, plot consistency, and story arc progression.

## Features

### Core Story Bible Management
- **Narrative Structure**: Create and manage story outlines, plot points, and narrative arcs
- **Character Development**: Track character backgrounds, motivations, relationships, and growth
- **Scene Management**: Organize scenes, locations, and sequences
- **Plot Consistency**: Ensure story coherence and continuity checking
- **Theme Tracking**: Manage story themes, motifs, and symbolic elements

### MCP Tools Available
- `create_story_bible(project_id, title, genre, premise)` - Initialize new story bible
- `add_character(story_bible_id, character_data)` - Add character to story bible
- `create_story_outline(story_bible_id, outline_data)` - Create story structure
- `add_scene(story_bible_id, scene_data)` - Add scene information
- `track_plot_thread(story_bible_id, thread_data)` - Manage plot threads
- `validate_story_consistency(story_bible_id)` - Check for plot holes and inconsistencies
- `generate_character_arc(character_id)` - AI-assisted character development
- `suggest_scene_transitions(story_bible_id, scene_id)` - Scene flow optimization

## System Integration

### Brain Service Connection
- **Knowledge Graph**: Character relationships stored in Neo4j via MCP Brain Service
- **Semantic Search**: Find similar story elements using Jina v4 embeddings
- **Cross-Reference**: Link to existing characters, locations, and plot elements

### LangGraph Orchestrator Integration
- **Workflow Coordination**: Receive story generation requests from orchestrator
- **Agent Collaboration**: Work with Character, Visual, and Audio MCP services
- **Progress Tracking**: Report story bible creation progress to orchestrator

## Technology Stack

### Core Technologies
- **Python 3.11+** - Core service implementation
- **FastAPI** - REST API and WebSocket endpoints
- **MCP Protocol** - Model Context Protocol implementation
- **Pydantic** - Data validation and serialization
- **SQLAlchemy** - Local database ORM for story bible data
- **PostgreSQL** - Primary database for story bible storage

### AI Integration
- **Brain Service MCP Client** - Connect to centralized AI services
- **Story Generation AI** - LLM integration for story suggestions
- **Consistency Checking** - AI-powered plot hole detection
- **Character Development** - AI-assisted character arc creation

### Development & Deployment
- **Docker** - Containerized deployment
- **pytest** - Testing framework  
- **Black** - Code formatting
- **mypy** - Type checking
- **GitHub Actions** - CI/CD pipeline

## Environment Configuration

### Local Development
```bash
# Service Configuration
PORT=8015
HOST=0.0.0.0
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql://story_bible:password@localhost:5432/story_bible_db

# MCP Brain Service Connection
BRAIN_SERVICE_URL=http://localhost:8002
BRAIN_SERVICE_WS_URL=ws://localhost:8002/mcp

# Authentication (if needed)
API_KEY_SECRET=your-secret-key-here
```

### Production Configuration
```bash
# Production endpoints
BRAIN_SERVICE_URL=https://brain.ft.tc
BRAIN_SERVICE_WS_URL=wss://brain.ft.tc/mcp
DATABASE_URL=postgresql://story_bible:prod_password@prod_host/story_bible_db
```

## Quick Start

### Local Development
```bash
# Clone and setup
git clone https://github.com/jomapps/mcp-story-bible-service.git
cd mcp-story-bible-service

# Setup virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup database
python scripts/init_db.py

# Start service
python -m src.main
```

### Using Docker
```bash
# Build and run
docker-compose up -d

# Check health
curl http://localhost:8015/health
```

## API Endpoints

### Health & Status
- `GET /health` - Service health check
- `GET /status` - Detailed service status
- `GET /metrics` - Service metrics (Prometheus format)

### MCP Integration
- `WebSocket /mcp` - MCP protocol endpoint
- `POST /mcp/tools` - Available MCP tools list
- `POST /mcp/call` - Direct MCP tool invocation

### REST API
- `POST /api/v1/story-bibles` - Create new story bible
- `GET /api/v1/story-bibles/{id}` - Get story bible details  
- `PUT /api/v1/story-bibles/{id}` - Update story bible
- `DELETE /api/v1/story-bibles/{id}` - Delete story bible

## Data Models

### Story Bible Structure
```python
class StoryBible(BaseModel):
    id: str
    project_id: str
    title: str
    genre: str
    premise: str
    logline: str
    treatment: Optional[str]
    characters: List[Character]
    scenes: List[Scene]  
    plot_threads: List[PlotThread]
    themes: List[str]
    created_at: datetime
    updated_at: datetime

class Character(BaseModel):
    id: str
    name: str
    role: str  # "protagonist", "antagonist", "supporting"
    background: str
    motivation: str
    arc_description: str
    relationships: List[CharacterRelationship]

class Scene(BaseModel):
    id: str
    sequence_number: int
    location: str
    time_of_day: str
    characters_present: List[str]
    scene_purpose: str
    description: str
    dialogue_notes: str
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run integration tests
pytest tests/integration/

# Test MCP protocol
python scripts/test_mcp_tools.py
```

## Monitoring

### Health Monitoring
- Service uptime and response times
- Database connection status  
- MCP Brain Service connectivity
- Story bible creation success rates

### Metrics Collection
- Number of active story bibles
- Average story bible completion time
- Character relationship complexity
- Plot consistency scores

## Related Services

- **[MCP Brain Service](../mcp-brain-service)** - Knowledge graph and embeddings
- **[LangGraph Orchestrator](../langgraph-orchestrator)** - Workflow coordination
- **[Auto-Movie App](../../apps/auto-movie)** - Frontend interface

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit pull request

## License

MIT License - See LICENSE file for details
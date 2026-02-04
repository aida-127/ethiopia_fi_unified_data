# Event Impact Modeling Methodology

## 1. Approach Overview
The event impact model estimates how specific events (product launches, policies, infrastructure investments) affect financial inclusion indicators over time. The model combines:
- **Actual impact links** from the dataset
- **Comparable country evidence** from literature
- **Expert judgment** for event-indicator relationships
- **Historical validation** using Ethiopian data

## 2. Impact Estimation Process

### Step 1: Categorize Events
Events are categorized by type:
- **Product Launch** (e.g., Telebirr, M-Pesa): Direct impact on usage metrics
- **Market Entry** (e.g., Safaricom Ethiopia): Competitive effects
- **Policy Change** (e.g., tax exemption, FX liberalization): Regulatory impacts
- **Infrastructure** (e.g., 5G launch, 4G expansion): Enabling effects

### Step 2: Estimate Base Impacts
Each event category has base impact estimates:
- **Product Launch**: +2.0pp on mobile money accounts (gradual over 12 months)
- **Market Entry**: +1.5pp on mobile money accounts (gradual over 12 months)
- **Policy**: +1.0pp on account ownership (gradual over 12 months)
- **Infrastructure**: +15pp on 4G coverage (immediate)

### Step 3: Apply Lag Effects
Different impacts have different lag times:
- **Immediate effects** (0-3 months): Infrastructure deployment, price changes
- **Short lag** (3-6 months): Policy implementation, product adoption
- **Long lag** (6-12 months): Behavior change, account ownership

### Step 4: Model Temporal Effects
Three effect models:
1. **Immediate**: Full effect at time of event
2. **Gradual**: Linear adoption over 12 months
3. **S-curve**: Logistic adoption pattern (slow start, rapid growth, plateau)

## 3. Validation Process

### Historical Validation
Compare model predictions with actual Ethiopian data:
- **Telebirr launch**: Predicted +2.0pp vs Actual +4.75pp on mobile money accounts
- Adjusted estimates based on validation results

### Comparable Country Evidence
Use evidence from similar contexts:
- **Kenya (M-Pesa)**: +7-10pp account ownership over 5 years
- **Tanzania (M-Pesa)**: +5-8pp account ownership over 4 years
- **Rwanda (cashless push)**: +15-20% digital transaction growth

## 4. Key Assumptions

### General Assumptions
1. **Additive effects**: Multiple event impacts sum linearly
2. **Independent events**: Event effects don't interact (simplifying assumption)
3. **Constant base trend**: Underlying growth trend separate from event effects
4. **Saturation limits**: Effects plateau after full adoption

### Ethiopia-Specific Assumptions
1. **High mobile penetration**: 61.4% mobile subscription enables digital finance
2. **Government support**: Pro-digital policies accelerate adoption
3. **Urban-rural divide**: Effects stronger in urban areas initially
4. **Gender considerations**: Effects may differ by gender

## 5. Limitations

### Data Limitations
1. **Sparse time series**: Limited pre/post event data points
2. **Aggregate data**: National averages mask regional variations
3. **Confounding factors**: Hard to isolate single event effects
4. **Lag uncertainty**: Exact timing of effects uncertain

### Model Limitations
1. **Simplified relationships**: Real-world dynamics more complex
2. **Constant parameters**: Don't capture changing market conditions
3. **No interaction effects**: Events may amplify or dampen each other
4. **External factors**: Macroeconomic conditions not modeled

## 6. Confidence Levels

### High Confidence
- Infrastructure deployment impacts (4G coverage)
- Price change effects (tax exemptions)
- Direct product adoption (registered users)

### Medium Confidence
- Account ownership changes
- Digital transaction growth
- Gender gap reductions

### Low Confidence
- Long-term behavioral changes
- Indirect/enabling effects
- Regional variations

/**
 * TimeInterval: Represents a time duration with days, hours, and parts (chalakim).
 * Used for durations of months, years, etc.
 */
export class TimeInterval {
  days: number;
  hours: number;
  parts: number;

  /** Parts per hour (class variable, can be configured) */
  static parts_in_hour: number = 1;
  static readonly HOURS_IN_DAY = 24;

  /**
   * Create a TimeInterval
   * @param days - Number of days (can be fractional)
   * @param hours - Number of hours (can be fractional)
   * @param parts - Number of parts/chalakim (can be fractional)
   * @param parts_in_hour - Optional: override parts_in_hour for this class
   */
  constructor(
    days: number = 0,
    hours: number = 0,
    parts: number = 0,
    parts_in_hour?: number
  ) {
    if (parts_in_hour && parts_in_hour !== 0) {
      TimeInterval.parts_in_hour = parts_in_hour;
    }

    this.days = days;
    this.hours = hours;
    this.parts = parts;
    this.reduce();
  }

  /**
   * Reduce: normalize the time interval so each unit is within valid bounds.
   * - Fractional days become hours
   * - Fractional hours become parts
   * - Hours >= 24 become days
   * - Parts >= parts_in_hour become hours
   */
  reduce(): void {
    // Convert fractional days into hours
    this.hours += (this.days % 1) * TimeInterval.HOURS_IN_DAY;
    this.days = Math.floor(this.days);

    // Convert fractional hours into parts
    this.parts += (this.hours % 1) * TimeInterval.parts_in_hour;
    this.hours = Math.floor(this.hours);

    // Reduce parts (subclass can override to handle sub-part units)
    this.reduceParts();

    // Carry whole hours, then normalize remaining parts
    this.hours += Math.floor(this.parts / TimeInterval.parts_in_hour);
    this.parts %= TimeInterval.parts_in_hour;

    // Carry whole days, then normalize remaining hours
    this.days += Math.floor(this.hours / TimeInterval.HOURS_IN_DAY);
    this.hours %= TimeInterval.HOURS_IN_DAY;
  }

  /**
   * Reduce parts (can be overridden in subclasses for finer granularity)
   */
  protected reduceParts(): void {
    // In base class, just truncate to integer
    this.parts = Math.floor(this.parts);
  }

  /** Iterate over components [days, hours, parts] */
  *[Symbol.iterator](): Generator<number> {
    yield this.days;
    yield this.hours;
    yield this.parts;
  }

  /** Get all components as array */
  toArray(): number[] {
    return [this.days, this.hours, this.parts];
  }

  /** Hash code for use in sets/maps */
  hashCode(): number {
    let hash = 0;
    for (const val of this.toArray()) {
      hash = ((hash << 5) - hash) + val;
      hash = hash & hash; // Convert to 32bit integer
    }
    hash = ((hash << 5) - hash) + TimeInterval.parts_in_hour;
    return hash & hash;
  }

  /** String representation: "days hours parts" */
  toString(): string {
    return `${this.days} ${String(this.hours).padStart(2, ' ')} ${String(this.parts).padStart(4, ' ')}`;
  }

  /** Debug representation */
  [Symbol.for('nodejs.util.inspect.custom')](): string {
    return `TimeInterval(${this.days}, ${this.hours}, ${this.parts}, parts_in_hour=${TimeInterval.parts_in_hour})`;
  }

  // ==================== Comparison Operators ====================

  equals(other: TimeInterval | any): boolean {
    if (!(other instanceof TimeInterval)) return false;

    const thisArr = this.toArray();
    const otherArr = other.toArray();

    for (let i = 0; i < Math.max(thisArr.length, otherArr.length); i++) {
      const a = thisArr[i] ?? 0;
      const b = otherArr[i] ?? 0;
      if (a !== b) return false;
    }
    return true;
  }

  greaterThan(other: TimeInterval): boolean {
    const thisArr = this.toArray();
    const otherArr = other.toArray();

    for (let i = 0; i < Math.max(thisArr.length, otherArr.length); i++) {
      const a = thisArr[i] ?? 0;
      const b = otherArr[i] ?? 0;
      if (a > b) return true;
      if (a < b) return false;
    }
    return false;
  }

  greaterThanOrEqual(other: TimeInterval): boolean {
    return this.greaterThan(other) || this.equals(other);
  }

  lessThan(other: TimeInterval): boolean {
    const thisArr = this.toArray();
    const otherArr = other.toArray();

    for (let i = 0; i < Math.max(thisArr.length, otherArr.length); i++) {
      const a = thisArr[i] ?? 0;
      const b = otherArr[i] ?? 0;
      if (a < b) return true;
      if (a > b) return false;
    }
    return false;
  }

  lessThanOrEqual(other: TimeInterval): boolean {
    return this.lessThan(other) || this.equals(other);
  }

  // ==================== Math Operators ====================

  add(addend: TimeInterval): TimeInterval {
    const result = this.toArray();
    const otherArr = addend.toArray();

    for (let i = 0; i < Math.max(result.length, otherArr.length); i++) {
      result[i] = (result[i] ?? 0) + (otherArr[i] ?? 0);
    }

    return new TimeInterval(...result);
  }

  subtract(subtrahend: TimeInterval): TimeInterval {
    const result = this.toArray();
    const otherArr = subtrahend.toArray();

    for (let i = 0; i < Math.max(result.length, otherArr.length); i++) {
      result[i] = (result[i] ?? 0) - (otherArr[i] ?? 0);
    }

    return new TimeInterval(...result);
  }

  multiply(factor: number): TimeInterval {
    const result = this.toArray().map(x => x * factor);
    return new TimeInterval(...result);
  }

  divide(divisor: number | TimeInterval): number | TimeInterval {
    if (divisor instanceof TimeInterval) {
      // Ratio: compute as combined fractions
      const thisArr = this.toArray();
      const otherArr = divisor.toArray();
      const PARTS_IN_HOUR = TimeInterval.parts_in_hour;
      const HOURS_IN_DAY = TimeInterval.HOURS_IN_DAY;

      let numerator = 0;
      let denominator = 0;

      // Combine: days * (HOURS_IN_DAY * PARTS_IN_HOUR) + hours * PARTS_IN_HOUR + parts
      numerator = thisArr[0] * HOURS_IN_DAY * PARTS_IN_HOUR +
                  (thisArr[1] ?? 0) * PARTS_IN_HOUR +
                  (thisArr[2] ?? 0);

      denominator = otherArr[0] * HOURS_IN_DAY * PARTS_IN_HOUR +
                    (otherArr[1] ?? 0) * PARTS_IN_HOUR +
                    (otherArr[2] ?? 0);

      return denominator !== 0 ? numerator / denominator : 0;
    } else {
      // Scalar division: return FineTimeInterval
      const result = this.toArray().map(x => x / divisor);
      return new FineTimeInterval(...result, 0, divisor);
    }
  }

  negate(): TimeInterval {
    return this.multiply(-1);
  }

  absolute(): TimeInterval {
    if (this.lessThan(new TimeInterval(0))) {
      return this.negate();
    }
    return this;
  }
}

/**
 * TimeInWeek: A time of week (1-7 for Sunday-Saturday), or offset.
 * Wraps days to 1-7 (where 7 is Shabbat/day 0).
 */
export class TimeInWeek extends TimeInterval {
  /**
   * Create a TimeInWeek
   * @param days - Day of week (will be normalized to 1-7)
   * @param hours - Hours
   * @param parts - Parts
   */
  constructor(days: number = 0, hours: number = 0, parts: number = 0) {
    super(days, hours, parts);
  }

  /**
   * Override reduce to normalize day to 1-7 (7 = Shabbat)
   */
  override reduce(): void {
    super.reduce();

    // Normalize days to 1-7
    this.days = this.days % 7;
    // We want Shabbos (day 0 mod 7) to appear as 7
    if (this.days === 0) {
      this.days = 7;
    }
  }
}

/**
 * FineTimeInterval: Time interval with sub-part precision (moments).
 * Used when dividing intervals.
 */
export class FineTimeInterval extends TimeInterval {
  moments: number;

  /** Moments per part (class variable, set on division) */
  static moments_in_part: number = 1;

  /**
   * Create a FineTimeInterval
   * @param days - Days
   * @param hours - Hours
   * @param parts - Parts
   * @param moments - Sub-part moments
   * @param moments_in_part - Optional: override moments_in_part for this class
   */
  constructor(
    days: number = 0,
    hours: number = 0,
    parts: number = 0,
    moments: number = 0,
    moments_in_part?: number
  ) {
    if (moments_in_part && moments_in_part !== 0) {
      FineTimeInterval.moments_in_part = moments_in_part;
    }

    super(days, hours, parts);
    this.moments = moments;
    this.reduce();
  }

  /**
   * Override reduceParts to handle moments
   */
  protected override reduceParts(): void {
    // Convert fractional parts to moments
    this.moments += (this.parts % 1) * FineTimeInterval.moments_in_part;
    this.parts = Math.floor(this.parts);

    // Truncate fractional moments
    this.moments = Math.floor(this.moments);

    // Carry whole parts from moments
    this.parts += Math.floor(this.moments / FineTimeInterval.moments_in_part);
    this.moments %= FineTimeInterval.moments_in_part;
  }

  /** Iterate over components [days, hours, parts, moments] */
  override *[Symbol.iterator](): Generator<number> {
    yield this.days;
    yield this.hours;
    yield this.parts;
    yield this.moments;
  }

  /** Get all components as array */
  override toArray(): number[] {
    return [this.days, this.hours, this.parts, this.moments];
  }

  /** String representation */
  override toString(): string {
    return `${this.days} ${String(this.hours).padStart(2, ' ')} ${String(this.parts).padStart(4, ' ')} ${String(this.moments).padStart(2, ' ')}`;
  }

  /** Debug representation */
  override [Symbol.for('nodejs.util.inspect.custom')](): string {
    return `FineTimeInterval(${this.days}, ${this.hours}, ${this.parts}, ${this.moments}, moments_in_part=${FineTimeInterval.moments_in_part})`;
  }

  /**
   * Division not supported for FineTimeInterval
   */
  override divide(divisor: number | TimeInterval): never {
    throw new TypeError(
      `Not supported for ${this.constructor.name}`
    );
  }
}

/**
 * Degrees and DegreesOfCircle from the timeInterval.py approach.
 * These use MeasureWithSubunits pattern (like TimeInterval does in calendarUnits).
 */
export class Degrees {
  static units: Record<string, number> = {
    degrees: 360,
    minutes: 60,
    seconds: 60,
  };
  static strict: boolean = false;

  degrees: number;
  minutes: number;
  seconds: number;

  constructor(degrees: number = 0, minutes: number = 0, seconds: number = 0) {
    this.degrees = degrees;
    this.minutes = minutes;
    this.seconds = seconds;
    this.reduce();
  }

  private reduce(): void {
    const MIN_PER_DEG = 60;
    const SEC_PER_MIN = 60;

    // Carry fractional degrees to minutes
    this.minutes += (this.degrees % 1) * MIN_PER_DEG;
    this.degrees = Math.floor(this.degrees);

    // Carry fractional minutes to seconds
    this.seconds += (this.minutes % 1) * SEC_PER_MIN;
    this.minutes = Math.floor(this.minutes);

    // Carry whole seconds back to minutes
    this.minutes += Math.floor(this.seconds / SEC_PER_MIN);
    this.seconds %= SEC_PER_MIN;

    // Carry whole minutes to degrees
    this.degrees += Math.floor(this.minutes / MIN_PER_DEG);
    this.minutes %= MIN_PER_DEG;
  }

  toString(): string {
    const roundedSec = this.seconds < 30 ? Math.floor(this.seconds) : Math.floor(this.seconds) + 1;
    return `${this.degrees}°${String(Math.floor(this.minutes)).padStart(2, '0')}'${String(roundedSec).padStart(2, '0')}"`;
  }

  *[Symbol.iterator](): Generator<number> {
    yield this.degrees;
    yield this.minutes;
    yield this.seconds;
  }

  toArray(): number[] {
    return [this.degrees, this.minutes, this.seconds];
  }

  equals(other: Degrees): boolean {
    if (this.degrees !== other.degrees || this.minutes !== other.minutes) return false;
    const thisRounded = Math.round(this.seconds);
    const otherRounded = Math.round(other.seconds);
    return thisRounded === otherRounded;
  }

  greaterThan(other: Degrees): boolean {
    if (this.degrees > other.degrees) return true;
    if (this.degrees < other.degrees) return false;
    if (this.minutes > other.minutes) return true;
    if (this.minutes < other.minutes) return false;
    return this.seconds > other.seconds;
  }

  lessThan(other: Degrees): boolean {
    if (this.degrees < other.degrees) return true;
    if (this.degrees > other.degrees) return false;
    if (this.minutes < other.minutes) return true;
    if (this.minutes > other.minutes) return false;
    return this.seconds < other.seconds;
  }

  greaterThanOrEqual(other: Degrees): boolean {
    return this.greaterThan(other) || this.equals(other);
  }

  lessThanOrEqual(other: Degrees): boolean {
    return this.lessThan(other) || this.equals(other);
  }

  add(other: Degrees): Degrees {
    return new Degrees(
      this.degrees + other.degrees,
      this.minutes + other.minutes,
      this.seconds + other.seconds
    );
  }

  subtract(other: Degrees): Degrees {
    return new Degrees(
      this.degrees - other.degrees,
      this.minutes - other.minutes,
      this.seconds - other.seconds
    );
  }

  multiply(factor: number): Degrees {
    return new Degrees(
      this.degrees * factor,
      this.minutes * factor,
      this.seconds * factor
    );
  }

  divide(divisor: number | Degrees): number | Degrees {
    if (divisor instanceof Degrees) {
      const thisVal = this.degrees * 3600 + this.minutes * 60 + this.seconds;
      const otherVal = divisor.degrees * 3600 + divisor.minutes * 60 + divisor.seconds;
      return otherVal !== 0 ? thisVal / otherVal : 0;
    } else {
      return new Degrees(
        this.degrees / divisor,
        this.minutes / divisor,
        this.seconds / divisor
      );
    }
  }

  negate(): Degrees {
    return this.multiply(-1);
  }

  absolute(): Degrees {
    if (this.lessThan(new Degrees(0))) {
      return this.negate();
    }
    return this;
  }

  round(): number {
    if (this.minutes < 30) {
      return this.degrees;
    } else {
      return this.degrees + 1;
    }
  }
}

/**
 * Degrees3: Degrees with thirds (finer precision than seconds)
 */
export class Degrees3 extends Degrees {
  thirds: number;

  constructor(degrees: number = 0, minutes: number = 0, seconds: number = 0, thirds: number = 0) {
    super(degrees, minutes, seconds);
    this.thirds = thirds;
  }

  override toArray(): number[] {
    return [this.degrees, this.minutes, this.seconds, this.thirds];
  }

  equals(other: Degrees): boolean {
    if (super.equals(other)) return true;

    if (!(other instanceof Degrees3)) {
      // Allow comparison with base Degrees
      return (
        this.degrees === other.degrees &&
        this.minutes === other.minutes &&
        (this.seconds === other.seconds ||
          (this.seconds + 1 === other.seconds && this.thirds < 30) ||
          (this.seconds === other.seconds + 1 && other.seconds >= 30))
      );
    }

    return (
      this.degrees === other.degrees &&
      this.minutes === other.minutes &&
      this.seconds === other.seconds &&
      this.thirds === other.thirds
    );
  }
}

/**
 * Degrees4: Degrees with fourths
 */
export class Degrees4 extends Degrees3 {
  fourths: number;

  constructor(
    degrees: number = 0,
    minutes: number = 0,
    seconds: number = 0,
    thirds: number = 0,
    fourths: number = 0
  ) {
    super(degrees, minutes, seconds, thirds);
    this.fourths = fourths;
  }

  override toArray(): number[] {
    return [this.degrees, this.minutes, this.seconds, this.thirds, this.fourths];
  }
}

/**
 * DegreesOfCircle: Degrees that wrap around 0-360
 */
export class DegreesOfCircle extends Degrees4 {
  static readonly DEGREES_IN_CIRCLE = 360;

  private circleReduce(): void {
    this.degrees = this.degrees % DegreesOfCircle.DEGREES_IN_CIRCLE;
    if (this.degrees < 0) {
      this.degrees += DegreesOfCircle.DEGREES_IN_CIRCLE;
    }
  }

  override add(other: Degrees): DegreesOfCircle {
    const result = new DegreesOfCircle(
      this.degrees + (other instanceof Degrees ? other.degrees : 0),
      this.minutes + (other instanceof Degrees ? other.minutes : 0),
      this.seconds + (other instanceof Degrees ? other.seconds : 0)
    );
    result.circleReduce();
    return result;
  }

  override subtract(other: Degrees): DegreesOfCircle {
    const result = new DegreesOfCircle(
      this.degrees - (other instanceof Degrees ? other.degrees : 0),
      this.minutes - (other instanceof Degrees ? other.minutes : 0),
      this.seconds - (other instanceof Degrees ? other.seconds : 0)
    );
    result.circleReduce();
    return result;
  }

  override multiply(factor: number): DegreesOfCircle {
    const result = new DegreesOfCircle(
      this.degrees * factor,
      this.minutes * factor,
      this.seconds * factor
    );
    result.circleReduce();
    return result;
  }
}
